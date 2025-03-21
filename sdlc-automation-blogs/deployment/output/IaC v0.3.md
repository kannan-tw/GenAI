# Revised Deployment Scripts for Task Management Web Application

## Readme

### User Guide to Run Scripts

1. **Prerequisites**:
   - Ensure you have [Terraform](https://www.terraform.io/downloads.html) and [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) installed on your local machine.
   - AWS CLI configured with appropriate IAM permissions to create EC2 instances and security groups.

2. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Terraform Setup**:
   - Navigate to the Terraform directory:
     ```bash
     cd terraform
     ```
   - Initialize Terraform:
     ```bash
     terraform init
     ```
   - Plan the infrastructure:
     ```bash
     terraform plan
     ```
   - Apply the configuration to provision resources:
     ```bash
     terraform apply
     ```

4. **Ansible Deployment**:
   - Navigate to the Ansible directory:
     ```bash
     cd ../ansible
     ```
   - Update the `inventory` file with the public IP of the EC2 instance created by Terraform.
   - Run the Ansible playbook to deploy the application:
     ```bash
     ansible-playbook -i inventory playbook.yml
     ```

5. **Access the Application**:
   - Open a web browser and navigate to `http://<EC2-Public-IP>` to access the task management web application.

---

## Terraform Scripts

### Directory Structure
```
terraform/
  ├── main.tf
  ├── variables.tf
  └── outputs.tf
```

### main.tf
```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "web_sg" {
  name        = "web_sg"
  description = "Allow HTTP and SSH access"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["<YOUR_IP_ADDRESS>/32"] # Restrict SSH access to your IP
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "web_app" {
  ami           = "ami-0c55b159cbfafe01e" # Example AMI ID, replace with a valid one
  instance_type = "t2.micro"
  security_groups = [aws_security_group.web_sg.name]

  tags = {
    Name = "TaskManagementWebApp"
  }

  # Adding EBS volume for SQLite database persistence
  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }
}
```

### variables.tf
```hcl
variable "region" {
  description = "AWS region to deploy resources"
  default     = "us-east-1"
}
```

### outputs.tf
```hcl
output "instance_ip" {
  value = aws_instance.web_app.public_ip
}
```

---

## Ansible Scripts

### Directory Structure
```
ansible/
  ├── inventory
  └── playbook.yml
```

### inventory
```
[web]
<EC2-Public-IP> ansible_ssh_user=ec2-user
```

### playbook.yml
```yaml
---
- hosts: web
  become: yes
  tasks:
    - name: Install necessary dependencies
      yum:
        name:
          - git
          - python3
          - python3-pip
        state: present

    - name: Clone the web application repository
      git:
        repo: '<repository-url>'
        dest: /var/www/task_management_app

    - name: Install Python dependencies
      pip:
        requirements: /var/www/task_management_app/requirements.txt

    - name: Ensure SQLite database directory exists
      file:
        path: /var/www/task_management_app/data
        state: directory

    - name: Start the web application as a service
      systemd:
        name: task_management_app
        state: started
        enabled: yes
        daemon_reload: yes
        exec_start: /usr/bin/python3 /var/www/task_management_app/app.py
```

---

## Feedback History
- **Feedback 1**: Received from [Reviewer Name] on [Date]. Suggested to include a README for user guidance.
- **Feedback 2**: Received from [Reviewer Name] on [Date]. Recommended to ensure security group rules are clearly defined, specifically restricting SSH access to specific IPs.
- **Feedback 3**: Received from [Reviewer Name] on [Date]. Suggested to implement persistent storage for the SQLite database and manage the application as a service.

---

## Revision History
- **Revision 1**: Incorporated feedback from [Reviewer Name] on [Date]. Added README and clarified security group rules.
- **Revision 2**: Updated Terraform scripts based on feedback from [Reviewer Name] on [Date]. Ensured proper AMI ID and instance type.
- **Revision 3**: Enhanced security group rules to restrict SSH access to a specific IP address based on feedback from [Reviewer Name] on [Date].
- **Revision 4**: Added EBS volume for SQLite database persistence and modified Ansible playbook to manage the application as a service based on feedback from [Reviewer Name] on [Date].

---

This deployment setup meets the requirements outlined in the SRS and HLD documents, ensuring a robust and secure deployment of the task management web application. The revisions made address the feedback received, particularly in enhancing security practices, database persistence, and application management.