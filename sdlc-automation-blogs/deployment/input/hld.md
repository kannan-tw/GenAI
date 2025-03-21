# High-Level Design (HLD)

## 1. Architecture Diagram
```
Internet --> EC2 Instance (Web App) --> SQLite Database (Local Storage)
```

## 2. Components
- **EC2 Instance**: Host for the web application.
- **Security Group**: Basic firewall rules allowing HTTP and SSH access.
- **SQLite Database**: Lightweight local database.

## 3. Deployment Strategy
- **Terraform** provisions the EC2 instance.
- **Ansible** installs necessary dependencies and deploys the application.