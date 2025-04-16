#!/usr/bin/env python3
import paramiko
import time
import os
import numpy as np
from PIL import Image
import logging
from logging.handlers import RotatingFileHandler

# Configure comprehensive logging with both console and file output
def setup_logging():
    """Configure logging to output to both console and file with rotation."""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Set up formatter
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

    # Set up console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Set up rotating file handler (10MB per file, max 5 backup files)
    file_handler = RotatingFileHandler(
        'logs/application.log',
        maxBytes=10*1024*1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[console_handler, file_handler]
    )

    logging.info("Logging system initialized with console and file handlers")

# Initialize logging
setup_logging()

# Part A: Remote Node Management using SSH
def ssh_execute_command(host, port, username, password, command):
    """Connect via SSH and execute a command on the remote host."""
    logging.debug(f"Attempting SSH connection to {host}:{port} with command: {command}")
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logging.debug(f"Connecting to {host}:{port} as {username}")
        
        client.connect(host, port=port, username=username, password=password, timeout=10)
        logging.info(f"SSH connection established to {host}:{port}")
        
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        err = stderr.read().decode()
        
        logging.debug(f"SSH command executed, processing output")
        if output:
            logging.info(f"Output from {host}:{port} -> {output.strip()}")
        if err:
            logging.error(f"Error from {host}:{port} -> {err.strip()}")
        
        client.close()
        logging.debug(f"SSH connection to {host}:{port} closed")
        return output, err
    except paramiko.AuthenticationException:
        logging.error(f"Authentication failed for {username}@{host}:{port}")
        return None, "Authentication failed"
    except paramiko.SSHException as e:
        logging.error(f"SSH connection error to {host}:{port}: {str(e)}")
        return None, str(e)
    except Exception as e:
        logging.error(f"Unexpected error connecting to {host}:{port}: {str(e)}")
        return None, str(e)

def simulate_node_shutdown(node_ip, port):
    """Simulate node shutdown (restart) using SSH command."""
    logging.info(f"Initiating simulated shutdown for node {node_ip}:{port}")
    command = "echo 'Simulated shutdown: Node will restart in 10 seconds'; sleep 10; echo 'Node restarted'"
    logging.debug(f"Executing shutdown simulation command: {command}")
    output, err = ssh_execute_command(node_ip, port, "root", "password", command)
    
    if output:
        logging.info(f"Shutdown simulation completed for {node_ip}:{port}")
    else:
        logging.error(f"Shutdown simulation failed for {node_ip}:{port}")
    return output

# Part B: RAID 5 & Alternate RAID 6
def split_image(image_path):
    """
    Split the image into three equal parts (R1, R2, R3) along the width.
    If the width isn't perfectly divisible by 3, each segment is truncated
    to the minimum width among them.
    """
    logging.info(f"Processing image: {image_path}")
    try:
        image = Image.open(image_path).convert("RGB")
        np_image = np.array(image)
        h, w, c = np_image.shape
        segment_width = w // 3

        logging.debug(f"Original image dimensions: {h}x{w}x{c}")
        logging.debug(f"Calculated segment width: {segment_width}")

        # Extract three segments
        R1 = np_image[:, :segment_width, :]
        R2 = np_image[:, segment_width:2*segment_width, :]
        R3 = np_image[:, 2*segment_width:2*segment_width + segment_width, :]

        # Ensure all segments have the same width
        min_width = min(R1.shape[1], R2.shape[1], R3.shape[1])
        R1 = R1[:, :min_width, :]
        R2 = R2[:, :min_width, :]
        R3 = R3[:, :min_width, :]

        logging.info(f"Successfully split image into three segments (width={min_width}).")
        logging.debug(f"Segment shapes - R1: {R1.shape}, R2: {R2.shape}, R3: {R3.shape}")
        return R1, R2, R3
    except Exception as e:
        logging.error(f"Error splitting image {image_path}: {str(e)}")
        raise

def compute_parity_raid5(R1, R2, R3):
    """Compute RAID5 parity: P = (R1 + R2 + R3) mod 256."""
    logging.debug("Computing RAID5 parity (R1 + R2 + R3 mod 256)")
    parity = (R1.astype(int) + R2.astype(int) + R3.astype(int)) % 256
    return parity.astype(np.uint8)

def compute_parity_raid6_alt(R1, R2, R3):
    """Compute alternate RAID6 parity: P = (R1 + R2 - R3) mod 256."""
    logging.debug("Computing alternate RAID6 parity (R1 + R2 - R3 mod 256)")
    parity = (R1.astype(int) + R2.astype(int) - R3.astype(int)) % 256
    return parity.astype(np.uint8)

def simulate_node_failure_and_recovery(image_path, failed_segment='R2',
                                     output_folder="output", use_alt_raid6=False):
    """
    Simulate a failure by removing one segment and reconstructing it using RAID parity.
    """
    logging.info(f"Starting failure simulation for image: {image_path}")
    logging.debug(f"Parameters - failed_segment: {failed_segment}, output_folder: {output_folder}, use_alt_raid6: {use_alt_raid6}")

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        logging.debug(f"Creating output directory: {output_folder}")
        os.makedirs(output_folder)

    try:
        # Split the image
        R1, R2, R3 = split_image(image_path)

        # Compute both parities for demonstration
        logging.info("Computing parity data")
        parity_raid5 = compute_parity_raid5(R1, R2, R3)         # R1 + R2 + R3
        parity_raid6 = compute_parity_raid6_alt(R1, R2, R3)     # R1 + R2 - R3

        # Choose which parity method to use
        if use_alt_raid6:
            chosen_parity = parity_raid6
            method_label = "RAID6-alt (R1+R2-R3)"
        else:
            chosen_parity = parity_raid5
            method_label = "RAID5 (R1+R2+R3)"

        logging.info(f"Selected recovery method: {method_label}")

        # Identify which segments are still available
        if failed_segment == 'R1':
            available1, available2 = R2, R3
            failed_label = "R1"
        elif failed_segment == 'R2':
            available1, available2 = R1, R3
            failed_label = "R2"
        elif failed_segment == 'R3':
            available1, available2 = R1, R2
            failed_label = "R3"
        else:
            logging.error("Invalid failed_segment specified. Use 'R1', 'R2', or 'R3'.")
            return

        logging.debug(f"Simulating failure of segment {failed_label}")
        logging.debug(f"Available segments: {available1.shape}, {available2.shape}")

        # Recovery logic
        if not use_alt_raid6:
            # RAID5 formula: P = R1 + R2 + R3
            logging.debug("Using RAID5 recovery formula")
            if failed_segment == 'R1':
                recovered = chosen_parity.astype(int) - available1.astype(int) - available2.astype(int)
            elif failed_segment == 'R2':
                recovered = chosen_parity.astype(int) - available1.astype(int) - available2.astype(int)
            else:  # R3
                recovered = chosen_parity.astype(int) - available1.astype(int) - available2.astype(int)
        else:
            # alt RAID6 formula: P = R1 + R2 - R3
            logging.debug("Using alternate RAID6 recovery formula")
            if failed_segment == 'R1':
                recovered = chosen_parity.astype(int) - available1.astype(int) + available2.astype(int)
            elif failed_segment == 'R2':
                recovered = chosen_parity.astype(int) + available2.astype(int) - available1.astype(int)
            else:  # R3
                recovered = available1.astype(int) + available2.astype(int) - chosen_parity.astype(int)

        # Convert to uint8 with mod 256
        recovered = (recovered % 256).astype(np.uint8)
        logging.info(f"Successfully recovered missing segment {failed_label} using {method_label}")

        # Reconstruct the full image
        if failed_segment == 'R1':
            reconstructed = np.concatenate((recovered, available1, available2), axis=1)
        elif failed_segment == 'R2':
            reconstructed = np.concatenate((available1, recovered, available2), axis=1)
        else:
            reconstructed = np.concatenate((available1, available2, recovered), axis=1)

        logging.debug(f"Reconstructed image shape: {reconstructed.shape}")

        # Save the recovered image
        base_name = os.path.basename(image_path)
        output_filename = os.path.join(output_folder, f"recovered_{base_name}")
        Image.fromarray(reconstructed).save(output_filename)
        logging.info(f"Successfully saved reconstructed image to '{output_filename}'")

    except Exception as e:
        logging.error(f"Error during failure simulation for {image_path}: {str(e)}")
        raise

# Part C: Process Images from train, test, valid
def process_image_folders(base_path="data", use_alt_raid6=False):
    """
    Process one sample image from each subfolder (train, test, valid)
    and perform RAID-based recovery.
    """
    logging.info(f"Processing image folders in {base_path}")
    logging.debug(f"use_alt_raid6 parameter: {use_alt_raid6}")
    
    folders = ["train", "test", "valid"]
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        logging.debug(f"Processing folder: {folder_path}")
        
        if not os.path.exists(folder_path):
            logging.error(f"Folder '{folder_path}' does not exist.")
            continue

        images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not images:
            logging.warning(f"No images found in folder '{folder_path}'.")
            continue

        image_path = os.path.join(folder_path, images[0])
        logging.info(f"Processing image '{image_path}' in folder '{folder}'")
        
        try:
            simulate_node_failure_and_recovery(
                image_path,
                failed_segment='R2',
                output_folder="output",
                use_alt_raid6=use_alt_raid6
            )
        except Exception as e:
            logging.error(f"Failed to process image {image_path}: {str(e)}")
            continue

# Part D: Main Orchestration
def main():
    try:
        logging.info("==== Starting application ====")
        
        # Step 1: Simulate a node shutdown via SSH
        logging.info("==== SIMULATING NODE SHUTDOWN ====")
        node_ip = "localhost"
        ssh_port = 2223
        shutdown_output = simulate_node_shutdown(node_ip, ssh_port)
        
        if shutdown_output:
            logging.info(f"Shutdown simulation output:\n{shutdown_output}")
        else:
            logging.warning("No output received from shutdown simulation")

        # Wait to simulate downtime and (hypothetical) Sensu update
        logging.info("Waiting 15 seconds to simulate node downtime and dashboard update...")
        time.sleep(15)
        logging.info("Resuming after simulated downtime")

        # Step 2: Process images from 'train', 'test', 'valid' using either RAID5 or alt RAID6
        logging.info("==== PROCESSING IMAGE FOLDERS ====")
        process_image_folders(base_path="data", use_alt_raid6=True)
        
        logging.info("==== Application completed successfully ====")
    except Exception as e:
        logging.error(f"Fatal error in main: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()