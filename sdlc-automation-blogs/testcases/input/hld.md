# High-Level Design (HLD)

## 1. Introduction

This document provides the high-level design for a web-based task management application, based on the Software Requirements Specification (SRS). The system is designed using a microservices architecture to ensure scalability, modularity, and maintainability.

## 2. Architectural Overview

The application will follow a microservices architecture, with services communicating through RESTful APIs or gRPC. Each service is designed to handle a specific set of responsibilities, ensuring a separation of concerns.

### 2.1 Core Components
- **API Gateway**: Acts as a single entry point for all client requests, routing them to appropriate microservices and handling cross-cutting concerns such as authentication and rate limiting.
- **Task Management Service**: Manages task-related operations such as creation, assignment, and status updates.
- **Notification Service**: Handles email and in-app notifications triggered by task events.
- **Reporting Service**: Aggregates task data to generate reports.
- **Database**: Centralized storage with logical separation for each microservice to maintain its own schema.

### 2.2 Technology Stack
- **Frontend**: Streamlit for building the user interface.
- **Backend**: Node.js with Express.js or Java (Spring Boot) for microservices.
- **Database**: PostgreSQL for relational data and Redis for caching.
- **Messaging**: RabbitMQ for asynchronous communication.

## 3. Microservices Design

### 3.1 API Gateway
- **Responsibilities**:
  - Route incoming requests to appropriate services.
  - Authenticate and authorize requests.
  - Provide rate limiting and monitoring.
- **Endpoints**:
  - `/tasks` -> Task Management Service.
  - `/notifications` -> Notification Service.
  - `/reports` -> Reporting Service.
  
### 3.2 Task Management Service
- **Responsibilities**:
  - CRUD operations for tasks.
  - Manage task assignments and status updates.
- **Endpoints**:
  - `POST /tasks` - Create a task.
  - `GET /tasks/{id}` - Retrieve task details.
  - `PUT /tasks/{id}` - Update task.
  - `DELETE /tasks/{id}` - Delete task.
- **Database Schema**:
  - `Tasks` table with fields: `id`, `title`, `description`, `status`, `priority`, `due_date`, `assignee_id`, `created_at`, `updated_at`.

### 3.3 Notification Service
- **Responsibilities**:
  - Process task events to send notifications.
  - Support email and in-app notifications.
- **Communication**:
  - Listens to task events via a message queue.
  - Publishes notification events.
- **Database Schema**:
  - `Notifications` table with fields: `id`, `user_id`, `task_id`, `type`, `message`, `status`, `created_at`.

### 3.4 Reporting Service
- **Responsibilities**:
  - Generate task-related reports based on user or team activities.
- **Communication**:
  - Queries the Task Management Service database.
  - Supports exporting reports in various formats (e.g., PDF, Excel).
- **Database Schema**:
  - Uses read-only replicas of the `Tasks` and `Users` tables.


## 4. Interaction Flow

### 4.1 Task Creation
1. User sends a `POST /tasks` request to the API Gateway.
2. The API Gateway forwards the request to the Task Management Service.
3. The Task Management Service validates and creates the task in the database.
4. A task creation event is sent to the Notification Service via the message queue.
5. The Notification Service sends notifications to relevant users.

### 4.2 Status Update
1. User sends a `PUT /tasks/{id}` request to update a task status.
2. The Task Management Service updates the status in the database.
3. A status update event is sent to the Notification Service.
4. The Notification Service triggers notifications for the status change.

### 4.3 Report Generation
1. User requests a report via `GET /reports`.
2. The API Gateway routes the request to the Reporting Service.
3. The Reporting Service queries the database for relevant data.
4. The generated report is returned to the user.

---

This High-Level Design document serves as a blueprint for developers to implement the task management application. Developers should refer to the SRS and HLD during development to ensure alignment with requirements.

