# Software Requirements Specification (SRS)

## 1. Introduction

### 1.1 Purpose
The purpose of this document is to define the software requirements for a web-based task management application. This application will facilitate capturing, status tracking, and managing tasks for users and teams, ensuring improved productivity and collaboration.

### 1.2 Scope
The web application will allow users to:
- Create and manage tasks.
- Assign tasks to users or teams.
- Track the status of tasks through predefined statuses (e.g., Open, In Progress, Completed).
- Receive notifications for updates on tasks.
- Generate reports on task progress and completion.

The application will integrate internal services for seamless operation, ensuring task management, notifications, and reporting work cohesively.

### 1.3 Audience
This document is intended for:
- Project stakeholders.
- Development team members.
- Quality assurance testers.
- System administrators.

## 2. Functional Requirements

### 2.1 Task Management
#### 2.1.1 Task Creation
- Users can create tasks with the following attributes:
  - Title (mandatory).
  - Description (optional).
  - Due date (optional).
  - Priority (e.g., Low, Medium, High).
  - Tags (optional).

#### 2.1.2 Task Assignment
- Tasks can be assigned to individual users or teams.
- Task owners can reassign tasks if necessary.

#### 2.1.3 Task Status Tracking
- Tasks can have statuses: Open, In Progress, Blocked, Completed, Archived.
- Users can update the status of tasks they own or are assigned to.

### 2.2 Notifications
- Email and in-app notifications will be sent for:
  - Task assignment.
  - Status changes.
  - Approaching due dates (configurable reminders).

### 2.3 Reporting
- Generate reports based on:
  - Task completion rates.
  - Overdue tasks.
  - Task distribution across team members.


## 3. Internal Service Dependencies

### 3.1 Notification Service
- The task management module will trigger notifications via the internal notification service.
- Dependencies:
  - The notification service must receive task updates and generate corresponding in-app or email notifications.


### 3.2 Task Management Core
- The task management core is the central module connecting all other services.
- Dependencies:
  - All updates to tasks (creation, assignment, status changes) must propagate to the notification and reporting services.
  

## 6. Assumptions and Dependencies
- Users will have active internet connections.
- Internal services (notification, reporting, user management) must be operational for full functionality.
- Team members will adhere to role-based permissions when assigning and managing tasks.

---

This document will serve as a reference throughout the project lifecycle to ensure alignment with requirements and project goals.

