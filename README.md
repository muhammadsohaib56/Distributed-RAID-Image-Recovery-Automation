# Distributed-RAID-Image-Recovery-Automation
A Python-based system that simulates remote node shutdowns, manages RAID Level 5 &amp; alternate Level 6 recovery for images, and uses Docker &amp; Supervisord for full automation and monitoring. Includes Sensu integration for real-time system health monitoring.

Sure! Here's a **professional and well-structured README.md** for your project **"Distributed RAID Image Recovery Automation"**:

---

# Distributed RAID Image Recovery Automation

> Automating fault-tolerant cloud storage using distributed RAID levels (5 & 6), image recovery, and monitoring with Dockerized microservices and Sensu.

---

## 📌 Project Description

This project simulates a **Mini Cloud Infrastructure** where **images are uploaded, stored across a distributed RAID setup**, and in case of failure, **RAID-5 and RAID-6** strategies are used to **recover missing/lost data**.

It demonstrates a **highly available, fault-tolerant, and automated image storage-recovery system** deployed in a **containerized microservices architecture** with **monitoring and supervision support**.

---

## ⚙️ How It Works

1. **User Uploads an Image**: The image is chunked and encoded using RAID-5 or RAID-6 parity logic.
2. **Storage Simulation**: The chunks are stored in simulated cloud directories (`cloud1`, `cloud2`, etc.).
3. **Image Deletion (Simulating Failure)**: One or more parts are deleted to mimic disk failure.
4. **Automated Recovery**: 
   - RAID-5 recovers from single disk failure.
   - RAID-6 recovers from two disk failures.
5. **Image is Reconstructed** and stored in the output directory.
6. **Monitoring**: Sensu monitors container and service health to ensure fault tolerance.

---

## 🛠 Tech Stack

| Technology       | Purpose                                     |
|------------------|---------------------------------------------|
| **Python**       | Main programming language                   |
| **Docker**       | Containerization of services                |
| **Docker Compose**| Service orchestration                       |
| **Sensu Go**     | Monitoring and alerting                     |
| **Supervisor**   | Process monitoring inside containers        |
| **RAID Algorithms**| RAID 5 and 6 for data protection           |
| **Linux Commands**| File simulation and process automation     |

---

## 📂 Folder Structure

```
cloud_proj/
│
├── data/                  # Input images
├── cloud1/, cloud2/, ... # Simulated cloud storages
├── output/                # Recovered images
│
├── docker-compose.yaml   # Orchestrates services
├── Dockerfile            # Builds app container
├── supervisord.conf      # Monitors services
├── cloud_storage.py      # Image splitting, recovery logic
├── agent.yml             # Sensu agent config
└── logs/                 # App and recovery logs
```

---

## 🔧 Tools & Technologies

- Docker & Docker Compose
- Python 3.x
- Sensu Go
- Supervisor
- Git & GitHub
- RAID 5 & RAID 6 Recovery Algorithms
- Linux shell commands for deletion simulation

---

## 🚀 Setup Instructions

> These steps will help you set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/muhammadsohaib56/Distributed-RAID-Image-Recovery-Automation.git
cd Distributed-RAID-Image-Recovery-Automation
```

### 2. Build Docker Containers

```bash
docker-compose build
```

### 3. Start Services

```bash
docker-compose up
```

This will:
- Launch your RAID cloud recovery services
- Start Supervisord to manage internal services
- Start Sensu for monitoring

### 4. Upload Image for Simulation

Place your test image inside the `data/` folder with `.jpg` or `.png` extension.

### 5. Run Image Recovery Logic

```bash
python3 cloud_storage.py
```

This will:
- Distribute the image into cloud parts
- Simulate RAID storage
- Delete cloud data to simulate failure
- Automatically recover using RAID-5 or RAID-6 logic
- Output the recovered image in `/output` folder

---

## ✅ Features

- ✅ RAID-5 recovery from 1 missing chunk
- ✅ RAID-6 recovery from 2 missing chunks
- ✅ Dockerized & isolated microservices
- ✅ Auto-recovery via Python
- ✅ Monitoring with Sensu
- ✅ Logging with Supervisor
- ✅ Cross-platform support

---

## 📡 Monitoring View (Sensu)

Sensu Agent successfully running and sending health checks of cloud storage containers and services. Ensures real-time monitoring and notification.

---

## 🤝 Contributing

Feel free to open issues or submit pull requests if you'd like to improve the project!

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Muhammad Sohaib**  
🔗 GitHub: [@muhammadsohaib56](https://github.com/muhammadsohaib56)  
💼 LinkedIn: [View Profile](https://www.linkedin.com/in/muhammad-sohaib-shoukat-7b4064218/)

---

## 📬 Contact

If you face any issues or have suggestions, feel free to open an issue or contact me.

```

---

Let me know if you’d like this exported as a `.md` file, or if you want a **badge version**, demo video link, or a one-click deploy badge for DockerHub/GitHub Actions!
