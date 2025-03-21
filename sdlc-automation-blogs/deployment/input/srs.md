# Software Requirements Specification (SRS)

## 1. Introduction
### 1.1 Purpose
This document specifies the functional requirements for the deployment of a simple task management web application using Terraform and Ansible.

### 1.2 Scope
- Deploy a web application on AWS.
- Use Terraform for infrastructure provisioning.
- Use Ansible for application deployment and configuration management.

## 2. Functional Requirements
1. Provision cloud resources (EC2 instance, Security Group, and basic networking).
2. Deploy a web application with a database backend.
3. Ensure secure access using basic SSH security groups.

## 3. Non-Functional Requirements
- Basic reliability and uptime.
- Minimal security configurations.