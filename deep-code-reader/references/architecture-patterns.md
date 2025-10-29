# Architecture Patterns Reference

## Overview

This reference catalogues common software architecture patterns to help identify and understand system designs quickly.

## Layered Patterns

### 1. Three-Tier / N-Tier Architecture

**Structure:**
```
Presentation Layer
    ↓
Business Logic Layer
    ↓
Data Access Layer
```

**Characteristics:**
- Clear separation of concerns
- Each layer only communicates with adjacent layers
- Easy to replace individual layers

**Common in:**
- Enterprise applications
- Web applications
- Traditional monoliths

**Indicators:**
- Folders: `controllers/`, `services/`, `repositories/`
- Clear layer dependencies
- DTOs for data transfer between layers

### 2. MVC (Model-View-Controller)

**Structure:**
```
View ←→ Controller ←→ Model
```

**Characteristics:**
- Separates UI, business logic, and data
- Controller mediates between view and model
- Popular in web frameworks

**Common in:**
- Web frameworks (Rails, Django, Laravel)
- Desktop applications
- Mobile apps

**Indicators:**
- Folders: `models/`, `views/`, `controllers/`
- Route definitions pointing to controllers
- Template files in views

### 3. MVP (Model-View-Presenter)

**Structure:**
```
View ←→ Presenter ←→ Model
```

**Characteristics:**
- Presenter handles all UI logic
- View is passive (no logic)
- Easier to test than MVC

**Common in:**
- Android apps (older style)
- Desktop applications
- Complex UI applications

**Indicators:**
- Presenter classes with view interfaces
- Passive view implementations
- Clear separation of UI and logic

### 4. MVVM (Model-View-ViewModel)

**Structure:**
```
View ←→ ViewModel ←→ Model
```

**Characteristics:**
- Data binding between View and ViewModel
- ViewModel exposes data and commands
- Popular with reactive frameworks

**Common in:**
- WPF applications
- Modern frontend frameworks
- Mobile apps (SwiftUI, Jetpack Compose)

**Indicators:**
- Observable properties
- Data binding syntax
- ViewModels folder

## Clean/Hexagonal Architecture

### Clean Architecture (Uncle Bob)

**Structure:**
```
Entities (Domain)
    ↓
Use Cases (Application)
    ↓
Interface Adapters (Controllers, Presenters)
    ↓
Frameworks & Drivers (DB, UI, External)
```

**Characteristics:**
- Dependencies point inward
- Domain is independent of frameworks
- High testability

**Common in:**
- Modern backend services
- Domain-driven applications
- Microservices

**Indicators:**
- Folders: `domain/`, `application/`, `infrastructure/`
- Dependency inversion (interfaces in domain)
- Clear separation of concerns

### Hexagonal Architecture (Ports & Adapters)

**Structure:**
```
       Ports (Interfaces)
            ↓
    Application Core
            ↓
    Adapters (Implementations)
```

**Characteristics:**
- Core business logic is isolated
- Ports define interfaces
- Adapters implement interfaces
- Interchangeable external dependencies

**Common in:**
- Domain-driven systems
- Microservices
- Systems with multiple integrations

**Indicators:**
- Port interfaces in core
- Adapter implementations
- Dependency injection heavy

## Microservices Patterns

### 1. API Gateway Pattern

**Structure:**
```
Client → API Gateway → [Service A, Service B, Service C]
```

**Characteristics:**
- Single entry point for clients
- Request routing and composition
- Cross-cutting concerns (auth, logging)

**Indicators:**
- Gateway service/module
- Route configuration
- Service discovery integration

### 2. Event-Driven Architecture

**Structure:**
```
Service A → Event Bus ← Service B
                ↓
             Service C
```

**Characteristics:**
- Asynchronous communication
- Loose coupling between services
- Event sourcing possible

**Common in:**
- Distributed systems
- Reactive systems
- Real-time applications

**Indicators:**
- Event publishers/subscribers
- Message queues (RabbitMQ, Kafka)
- Event handlers

### 3. CQRS (Command Query Responsibility Segregation)

**Structure:**
```
Commands → Write Model → Data Store
Queries → Read Model → Query Store
```

**Characteristics:**
- Separate read and write operations
- Different models for different needs
- Often paired with Event Sourcing

**Indicators:**
- Command handlers
- Query handlers
- Separate read/write databases

## Data Patterns

### 1. Repository Pattern

**Structure:**
```
Service → Repository Interface → Repository Implementation → Database
```

**Characteristics:**
- Abstracts data access
- Centralized query logic
- Easier to test and swap data sources

**Indicators:**
- Repository classes/interfaces
- Data access abstraction
- Generic repository base classes

### 2. Active Record

**Structure:**
```
Model (contains data + database methods)
```

**Characteristics:**
- Model objects contain data and persistence logic
- Direct database interaction in models
- Simple and intuitive

**Common in:**
- Rails, Laravel
- ORM-based systems

**Indicators:**
- Models with save(), find() methods
- Database logic in models
- Inheritance from base Record class

### 3. Data Mapper

**Structure:**
```
Entity (plain data) ← Mapper → Database
```

**Characteristics:**
- Entities are plain objects
- Mapper handles persistence
- Better separation of concerns

**Indicators:**
- Entity classes without persistence logic
- Mapper/DAO classes
- Clear separation

## Frontend Patterns

### 1. Flux / Redux

**Structure:**
```
Action → Dispatcher → Store → View
  ↑__________________________|
```

**Characteristics:**
- Unidirectional data flow
- Centralized state management
- Predictable state updates

**Indicators:**
- Actions, reducers, store
- Middleware for side effects
- Connect/subscribe patterns

### 2. Component-Based Architecture

**Structure:**
```
App
├── Header Component
├── Main Component
│   ├── Sidebar Component
│   └── Content Component
└── Footer Component
```

**Characteristics:**
- Reusable UI components
- Composition over inheritance
- Props for data flow

**Common in:**
- React, Vue, Angular
- Modern web applications

**Indicators:**
- Component files/folders
- Props and state
- Component hierarchy

## Messaging Patterns

### 1. Publish-Subscribe

**Structure:**
```
Publisher → Topic → [Subscriber A, Subscriber B, Subscriber C]
```

**Characteristics:**
- One-to-many communication
- Loose coupling
- Asynchronous

**Indicators:**
- Event emitters
- Subscription mechanisms
- Message brokers

### 2. Request-Reply

**Structure:**
```
Client ←→ Request/Reply ←→ Server
```

**Characteristics:**
- Synchronous communication
- Correlated request and response
- Timeout handling

**Indicators:**
- Request/response objects
- Correlation IDs
- Callback functions

## Scalability Patterns

### 1. Load Balancing

**Structure:**
```
Client → Load Balancer → [Server 1, Server 2, Server 3]
```

**Characteristics:**
- Distributes traffic across servers
- Improves availability and performance
- Multiple algorithms (round-robin, least-connections)

**Indicators:**
- Load balancer configuration
- Multiple server instances
- Health checks

### 2. Caching Layers

**Structure:**
```
Client → Cache → Application → Database
```

**Characteristics:**
- Reduces latency
- Decreases database load
- Multiple cache levels possible

**Common patterns:**
- Cache-aside
- Write-through
- Write-behind

**Indicators:**
- Redis/Memcached integration
- Cache decorators/middleware
- TTL configurations

## Pattern Recognition Checklist

Use this checklist when analyzing a codebase:

**Directory Structure:**
- [ ] Clear layer separation?
- [ ] Domain/business logic isolation?
- [ ] Test organization?

**Dependencies:**
- [ ] Dependency direction?
- [ ] Interface usage?
- [ ] External library patterns?

**Communication:**
- [ ] Synchronous vs asynchronous?
- [ ] Event-driven?
- [ ] REST/GraphQL/gRPC?

**Data Access:**
- [ ] Repository pattern?
- [ ] Active Record?
- [ ] ORM usage?

**Frontend:**
- [ ] Component-based?
- [ ] State management?
- [ ] Routing patterns?

## Hybrid Patterns

Real-world systems often combine multiple patterns:

### Example: Modern Web Application

```
Frontend (React + Redux)
    ↓
API Gateway
    ↓
Microservices (Clean Architecture)
    ↓
Event Bus (Pub-Sub)
    ↓
Databases (Repository Pattern)
```

### Example: E-commerce Platform

```
Web UI (MVC)
    ↓
API Layer (REST)
    ↓
Business Logic (Clean Architecture)
    ↓
CQRS (Commands + Queries)
    ↓
Event Sourcing
    ↓
Data Stores (Write + Read Models)
```

## Anti-Patterns to Watch For

### Big Ball of Mud
- No clear structure
- Tight coupling everywhere
- Hard to understand and modify

### God Object
- One class doing everything
- Violates single responsibility
- Hard to test

### Spaghetti Code
- Complex control flow
- Heavy interdependencies
- Difficult to follow

### Circular Dependencies
- Modules depending on each other
- Hard to test in isolation
- Indicates design issues

## Pattern Transition Indicators

### Monolith → Microservices
- Service boundaries emerging
- API contracts defined
- Database per service

### Anemic → Rich Domain Model
- Logic moving from services to entities
- Domain events appearing
- Validation in domain

### Synchronous → Event-Driven
- Message queues introduced
- Event handlers added
- Async processing patterns

## Quick Reference: Pattern Identification

| If you see... | Likely pattern |
|--------------|----------------|
| `controllers/`, `models/`, `views/` | MVC |
| `domain/`, `application/`, `infrastructure/` | Clean Architecture |
| `ports/`, `adapters/` | Hexagonal |
| Event emitters, subscribers | Pub-Sub / Event-Driven |
| `repositories/`, data interfaces | Repository Pattern |
| State management, actions, reducers | Flux/Redux |
| API Gateway, service mesh | Microservices |
| CQRS, command handlers | CQRS |
| Cache decorators, TTL configs | Caching Layer |
