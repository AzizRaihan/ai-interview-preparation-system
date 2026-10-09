## Q1: What are the key components of a High-Level Design (HLD)?
High-Level Design (HLD) defines the overall architecture of a system and provides a high-level view of how different components interact with each other.

It focuses on system structure, major modules, scalability, security, and technology choices.

Defines major system components, architecture layers, and integration points
Includes scalability, security, database, and infrastructure considerations for the overall system
Example: In an e-commerce application, HLD defines components like User Service, Product Service, Payment Gateway, Database, Cache, and Load Balancer, along with how they communicate within the system.

---

## Q2: How do you decide between a Monolithic and Microservices Architecture in HLD?
The choice between Monolithic and Microservices architecture depends on factors such as application size, scalability requirements, system complexity, and team structure.

A monolithic architecture is suitable for smaller and simpler applications, while microservices are preferred for large-scale and highly scalable systems.

Monolithic architecture is easier to develop and deploy but becomes difficult to scale and maintain as the system grows
Microservices provide independent scalability and flexibility but introduce higher operational and communication complexity
Example: A startup building an MVP may choose a monolithic architecture for faster development, whereas platforms like Netflix or Amazon use microservices to scale different services independently.

Rule of Thumb: Start monolithic (if small) -> refactor to microservices as the system grows.

---

## Q3: What are the trade-offs between a Relational and Non-Relational(NoSQL) database in an HLD?
The choice between Relational and NoSQL databases depends on factors such as data structure, scalability requirements, consistency needs, and application workload.

Relational databases are ideal for structured data and strong consistency, while NoSQL databases are preferred for scalability and flexible data models.

Relational databases provide ACID transactions, strong consistency, and support complex SQL queries for structured data
NoSQL databases offer flexible schemas, horizontal scalability, and high performance for large-scale distributed systems
Example: A banking system typically uses a relational database like MySQL or PostgreSQL for transactional consistency, while social media platforms often use NoSQL databases like MongoDB or Cassandra to handle massive volumes of unstructured data and high traffic.

---

## Q4: How do you ensure high availability in an HLD?
High availability ensures that a system remains operational and accessible even during failures or heavy traffic conditions.

It is achieved by eliminating single points of failure and designing the system with redundancy, failover, and distributed infrastructure.

Uses redundancy, replication, and load balancing to keep services available during failures
Implements failover mechanisms, monitoring, and disaster recovery strategies for reliability
Example: In a cloud-based application, traffic is distributed across multiple servers using a load balancer, and if one server fails, requests are automatically redirected to healthy instances without downtime.

---

## Q5: Explain the concept of load balancing in the context of HLD.
Load balancing is the process of distributing incoming network or application traffic across multiple servers to ensure optimal resource utilization, high availability, and better system performance.

It helps prevent any single server from becoming overloaded while improving scalability and fault tolerance.

Distributes requests across multiple servers to improve performance and reliability
Prevents server overload and ensures high availability by eliminating single points of failure
Example: In a web application, a load balancer like Nginx or AWS ELB distributes user requests among multiple application servers so that traffic is handled efficiently even during peak load.

---

## Q6: What are the key considerations for designing a scalable system in HLD?
Designing a scalable system involves ensuring that the application can efficiently handle increasing users, traffic, and data without performance degradation.

It requires distributing workloads, optimizing resource usage, and reducing bottlenecks across the system.

Uses techniques like horizontal scaling, caching, partitioning, and database replication to handle increased load
Improves performance and reliability through asynchronous processing and distributed infrastructure
Example: A video streaming platform uses CDNs for static content delivery, Redis for caching, and multiple application servers behind a load balancer to support millions of concurrent users.

---

## Q7: How do you handle security concerns in HLD?
Security in High-Level Design is achieved by incorporating protection mechanisms at every layer of the system architecture rather than treating security as an afterthought.

It involves securing user access, data transmission, APIs, and infrastructure to protect the system from unauthorized access and attacks.

Implements authentication, authorization, encryption, and secure API practices to protect system resources
Uses monitoring, logging, input validation, and zero-trust principles to detect and prevent security threats
Example: In a banking application, users authenticate using OAuth 2.0 with MFA, all communication is encrypted using HTTPS/TLS, and role-based access control ensures users can only access authorized resources.

---

## Q8: What is Database Indexing?
Database indexing is a technique used to improve the speed of data retrieval operations by creating a structured reference to data in a database table.
Indexes help databases locate records quickly without scanning the entire table.

Improves query performance and reduces data retrieval time significantly
Adds extra storage overhead and may slightly slow down insert or update operations
Example: In a banking application, an index on the account number field allows the system to quickly find customer accounts during transactions.

---

## Q9: What are the steps involved in designing an API in HLD?
Designing an API in HLD involves defining how different systems or clients will communicate with the application in a secure, scalable, and standardized way.

It requires careful planning of endpoints, data formats, authentication, error handling, and versioning.

Defines resources, endpoints, request/response formats, and communication standards for the system
Includes authentication, rate limiting, versioning, and proper documentation for secure and maintainable APIs
Example: In an e-commerce application, APIs like /users, /products, and /orders are designed with JSON responses, JWT-based authentication, and versioning such as /api/v1/orders for backward compatibility.

---

## Q10: How do you ensure data consistency across distributed systems in HLD?
Data consistency in distributed systems ensures that all nodes or services eventually maintain accurate and synchronized data even when multiple operations occur simultaneously.

The consistency approach depends on business requirements, system scalability, and availability needs.

Uses techniques like distributed transactions, idempotent operations, and conflict resolution to maintain consistent data
Chooses between strong consistency and eventual consistency based on system requirements and CAP theorem trade-offs
Example: In an online banking system, strong consistency is used to ensure account balances remain accurate during transactions, while a social media feed may use eventual consistency for better scalability and availability.

---

## Q11: What role does fault tolerance play in HLD?
Fault tolerance ensures that a system continues to function properly even when some components fail or become unavailable.

It improves system reliability by minimizing downtime and preventing failures from affecting the entire application.

Uses redundancy, replication, and failure isolation to keep the system operational during failures
Improves reliability and user experience through graceful degradation and recovery mechanisms
Example: In a microservices-based application, if the recommendation service fails, the main application can still function by temporarily disabling recommendations instead of bringing down the entire system.

---

## Q12: How do you design for disaster recovery in HLD?
Disaster recovery in HLD focuses on ensuring that the system can quickly recover and continue operating after major failures such as server crashes, data loss, or regional outages.

It involves backup strategies, data replication, failover mechanisms, and recovery planning to minimize downtime and data loss.

Uses backups, geo-replication, and automated failover systems to maintain business continuity
Defines recovery objectives like RPO and RTO to ensure fast and reliable system restoration
Example: A cloud application replicates its database across multiple regions, so if one data center fails, traffic is automatically redirected to another region with minimal downtime and data loss.

---

## Q13: Explain the concept of Event-Driven Architecture in HLD.
Event-Driven Architecture (EDA) is a design approach where system components communicate through events instead of direct synchronous calls, enabling loosely coupled and asynchronous interactions.

In this architecture, producers generate events, which are processed by consumers through an event broker or message queue.

Enables asynchronous communication and improves scalability by decoupling system components
Increases system resilience and flexibility, allowing services to evolve independently
Example: In an e-commerce system, when an order is placed, an event is published to Kafka or RabbitMQ, and different services like payment, inventory, and notification systems consume the event independently to perform their tasks.

---

## Q14: How does a cache know when it is full and decide what data to remove?
A cache continuously tracks its current memory usage whenever new data is added, updated, or removed.
Every cache entry has a size, and the cache manager maintains an internal counter of total memory consumption.

When new data is inserted, the cache first calculates the size of that data and adds it to the current memory usage
If the total memory exceeds the configured cache limit, the cache immediately triggers an eviction policy like LRU or LFU to free space
Example: Suppose Redis cache has a limit of 1 GB and is currently using 950 MB. If a new object of 100 MB is added, Redis detects that total usage becomes 1.05 GB, which exceeds the limit. The cache then automatically removes older or less-used entries until memory usage goes below 1 GB again.

---

## Q15: How do you handle concurrency control in HLD?
Concurrency control in HLD ensures that multiple users or processes can safely access and modify shared data without causing inconsistencies or conflicts.

It uses techniques like locking, isolation levels, and MVCC to maintain data integrity during simultaneous operations.

Prevents issues like dirty reads, lost updates, and inconsistent data states during concurrent access
Uses locking mechanisms, isolation levels, or MVCC based on system requirements and workload patterns
Example: In a banking application, concurrency control ensures that two users cannot simultaneously update the same account balance incorrectly during fund transfers or withdrawals.

---

## Q16: What are the principles of RESTful API design in HLD?
RESTful API design follows a set of architectural principles that enable scalable, standardized, and easy-to-maintain communication between clients and servers.

It focuses on resource-based communication, stateless interactions, and proper usage of HTTP standards.

Uses resource-oriented URIs, standard HTTP methods, and status codes for consistent API communication
Ensures scalability and maintainability through statelessness, versioning, and content negotiation
Example: In a user management system, APIs like GET /users/1, POST /users, and DELETE /users/1 follow REST principles by treating users as resources and using appropriate HTTP methods for operations.

---

## Q17: Explain the role of a message broker in HLD and give examples.
A message broker is a middleware component that enables asynchronous communication between different services or applications by receiving, storing, and forwarding messages.

It helps decouple system components, improving scalability, reliability, and fault tolerance in distributed systems.

Enables asynchronous communication and loose coupling between services
Improves scalability, reliability, and fault isolation through message buffering and delivery management
Example: In an e-commerce application, when an order is placed, a message broker like Kafka or RabbitMQ sends events to inventory, payment, and notification services independently without direct service-to-service communication.

---

## Q18: What is Database Replication?
Database replication is the process of copying and maintaining the same data across multiple database servers to improve availability, reliability, and performance.
It helps systems continue functioning even if one database server fails.

Improves fault tolerance and high availability by maintaining multiple copies of data
Enhances read scalability by distributing read requests across replica databases
Example: In an e-commerce platform, the primary database handles writes, while replica databases serve read requests like product searches and order history.

---

## Q19: What are the considerations for designing a fault-tolerant network infrastructure in HLD?
A fault-tolerant network infrastructure is designed to keep the system operational even when network components, servers, or connections fail.

It focuses on redundancy, traffic management, isolation, and disaster recovery to ensure reliability and continuous service availability.

Uses redundant network paths, load balancing, and dynamic routing to avoid single points of failure
Implements isolation, security mechanisms, and disaster recovery strategies to maintain system stability during failures
Example: In a cloud-based application, if one data center or network route becomes unavailable, traffic is automatically redirected through backup routes and standby servers to ensure uninterrupted service.

---

## Q20: What role does containerization play in HLD, and how does it benefit system architecture?
Containerization packages applications and their dependencies into isolated containers, ensuring consistent execution across different environments.

It improves scalability, deployment efficiency, and reliability, making it highly suitable for modern distributed and microservices-based architectures.

Provides environment consistency, resource efficiency, and easy scalability through container orchestration platforms like Kubernetes
Supports microservices architecture by isolating services and improving deployment, maintenance, and fault isolation
Example: In a microservices application, each service such as authentication, payment, and notification runs inside separate Docker containers, allowing independent deployment and scaling without affecting other services.

---

## Q21: How do you design for data privacy and protection in HLD?
Designing for data privacy and protection involves securing sensitive information throughout its lifecycle and ensuring that only authorized users can access it.

It requires implementing encryption, access controls, compliance standards, and continuous monitoring to protect data from unauthorized access and breaches.

Uses encryption, access control mechanisms, and data masking techniques to secure sensitive information
Ensures compliance, auditing, and regular security assessments to maintain data privacy and system trust
Example: In a healthcare application, patient records are encrypted using AES, access is restricted through role-based permissions, and all data access activities are logged to comply with regulations like HIPAA.

---

## Q22: Explain the concept of a distributed cache in HLD and its advantages.
A distributed cache is a caching system where cached data is stored across multiple servers or nodes instead of a single machine, allowing faster and scalable data access in distributed applications.

It helps reduce database load and improves application performance by serving frequently accessed data from memory.

Improves response time and scalability by distributing cached data across multiple nodes
Reduces database load and provides fault tolerance through cache replication and distribution
Example: In an e-commerce platform, frequently accessed product details are stored in a distributed cache like Redis Cluster, enabling faster responses even during high traffic periods.

---

## Q23: How do you ensure data integrity in an HLD, and what techniques can be employed?
Data integrity in HLD ensures that data remains accurate, consistent, and reliable throughout its lifecycle, even during failures or concurrent operations.

It is maintained through validation, database constraints, transactions, and secure data handling practices.

Uses constraints, validation, and ACID transactions to maintain consistency and prevent invalid data operations
Employs checksums, encryption, logging, and error handling to detect and protect against data corruption or inconsistencies
Example: In a banking system, database transactions ensure that money is deducted from one account and credited to another atomically, preventing partial or inconsistent updates during fund transfers.

---

## Q24: How does the CAP theorem affect the design of a distributed database?
The CAP theorem states that a distributed system can guarantee only two out of three properties: Consistency, Availability, and Partition Tolerance.

It helps architects decide the trade-offs a distributed database should make based on business and system requirements.

CP systems prioritize consistency and partition tolerance, while AP systems prioritize availability and partition tolerance
The database design choice depends on whether the application values strict consistency or continuous availability more
Example: A banking application typically prefers consistency to ensure accurate transactions, while a social media platform may prioritize availability so users can continue accessing the system even during network failures.

---

## Q25: How is Horizontal Scaling different from Vertical Scaling?
Scaling is the process of increasing a system's capacity to handle higher traffic, users, or workloads. Horizontal and Vertical scaling are two common approaches used in system design.

Horizontal scaling adds more machines to the system, while vertical scaling increases the power of an existing machine.

Horizontal scaling increases capacity by adding more servers, improving scalability and fault tolerance
Vertical scaling upgrades existing hardware resources like CPU, RAM, or storage, but has hardware limitations
Example: A social media platform may use horizontal scaling by adding multiple application servers behind a load balancer, while a small application may use vertical scaling by upgrading a single server's RAM and CPU.

---

## Q26: What is Rate Limiting?
Rate limiting is a technique used to control the number of requests a client can send to a server within a specific time period.
It protects systems from abuse, excessive traffic, and denial-of-service attacks.

Prevents server overload and ensures fair resource usage among users
Improves system stability and security by controlling API traffic
Example: A public API may allow only 100 requests per minute per user to prevent misuse and maintain performance.

---

## Q27: Explain the concepts of latency, throughput, and availability in system design.
Latency, throughput, and availability are important metrics used to measure the performance and reliability of a system. These factors help determine how efficiently a system handles user requests and stays operational.

Latency measures response delay, throughput represents the amount of work handled, and availability defines how often the system remains accessible.

Latency refers to the time taken by the system to process and respond to a request
Throughput measures the number of requests handled in a given time, while availability indicates system uptime and reliability
Example: In a video streaming platform, low latency ensures videos start quickly, high throughput allows millions of users to stream simultaneously, and high availability keeps the service accessible without interruptions.

---

## Q28: How does sharding differ from database partitioning?
Sharding and partitioning are techniques used to divide large datasets into smaller parts for better performance and manageability. Although both split data, they differ in how and where the data is distributed.

Partitioning usually divides data within the same database system, while sharding distributes data across multiple database servers.

Partitioning organizes data into smaller sections inside a single database instance
Sharding spreads data across multiple servers to improve scalability and handle massive workloads
Example: A company may partition customer records by region within one database, but a large social media platform may shard user data across multiple servers to support millions of active users worldwide.

---

## Q29: Explain caching and the different cache update strategies used in system design.
Caching is a technique used to temporarily store frequently accessed data in fast memory so that future requests can be served quickly without repeatedly querying the main database or backend service.

It helps reduce response time, lowers server load, and improves the overall efficiency of the application.

Common cache update strategies include Write-Through, Write-Back, Cache-Aside, and Write-Around caching
The choice of strategy depends on factors like consistency requirements, read/write patterns, and performance needs
Example: In an e-commerce application, frequently viewed product details may be stored in Redis cache. When a product is updated, the cache can either be updated immediately (Write-Through) or refreshed only when needed (Cache-Aside).

---

## Q30: Explain the concept of a Content Delivery Network (CDN) in system design.
A Content Delivery Network (CDN) is a distributed network of servers that stores and delivers cached content from locations closer to end users.

Its main goal is to reduce loading time, decrease server traffic, and provide faster content delivery across different geographic regions.

Delivers static content like images, videos, and files from nearby edge servers for quicker access
Reduces load on the main server and improves application performance during heavy traffic
Example: When a user watches videos on a streaming platform, the CDN serves the content from the nearest edge server instead of the origin server, resulting in faster playback and lower latency.

---

## Q31: Explain the concept of leader election in distributed systems.
Leader election is a process in distributed systems where one node is selected as the coordinator or leader to manage specific tasks and make centralized decisions for the cluster.

The elected leader handles responsibilities like coordination, synchronization, task scheduling, and maintaining consistency among nodes.

Ensures that only one node performs critical coordination tasks at a given time
Helps maintain consistency and avoid conflicts in distributed environments
Example: In a distributed database cluster, one server may be elected as the leader to manage write operations, while other nodes act as followers and replicate the data.

---

## Q32: How do message queues like Kafka and RabbitMQ improve system design?
Message queues like Kafka and RabbitMQ are communication mechanisms that allow different services or components to exchange data asynchronously without directly depending on each other.

They help systems process tasks more efficiently by decoupling services and managing high volumes of requests smoothly.

Enable asynchronous communication between services, reducing direct dependency and system bottlenecks
Improve scalability and reliability by buffering messages and handling traffic spikes efficiently
Example: In a food delivery application, once an order is placed, a message queue sends events separately to payment, notification, and delivery services so each task can be processed independently without slowing down the main application.

---

## Q33: Differentiate between synchronous and asynchronous communication in distributed systems.
Synchronous and asynchronous communication are two ways services interact in distributed systems. The main difference lies in whether the sender waits for an immediate response or continues processing independently.

Synchronous communication waits for a reply before moving forward, while asynchronous communication allows tasks to continue without blocking.

In synchronous communication, the client waits for the server response, leading to tighter coupling and possible delays
In asynchronous communication, requests are processed independently, improving scalability and responsiveness
Example: A payment verification API is usually synchronous because the user waits for confirmation instantly, whereas email notifications are commonly asynchronous and processed later through message queues like Kafka or RabbitMQ.

---

## Q34: Explain how you would design an API Gateway.
An API Gateway acts as a single entry point for client requests in a microservices architecture. It receives requests from clients and routes them to the appropriate backend services.

It also handles common functionalities like authentication, rate limiting, logging, and request aggregation.

Centralizes request routing, authentication, monitoring, and traffic management for multiple services
Reduces complexity for clients by providing a unified interface to backend microservices
Example: In an e-commerce platform, the API Gateway receives requests from mobile and web applications and forwards them to services like user management, product catalog, and payment processing while also validating JWT tokens and applying rate limits.

---

## Q35: What is the Circuit Breaker Pattern?
The Circuit Breaker Pattern is a fault-tolerance design pattern used in distributed systems to prevent repeated requests to a failing service.
It improves system resilience by stopping cascading failures during outages.

Prevents unnecessary calls to failed services and allows systems to recover gracefully
Improves reliability and response time during partial system failures
Example: In a microservices application, if the payment service becomes unavailable, the circuit breaker temporarily blocks requests and returns fallback responses instead of repeatedly retrying failed calls.

---

## Q36: Explain Consistent Hashing.
Consistent hashing is a distributed hashing technique used to evenly distribute data across multiple servers while minimizing data movement when servers are added or removed.
It is commonly used in distributed caching and database sharding systems.

Reduces data redistribution when scaling servers up or down
Improves scalability and load distribution in distributed systems
Example: Distributed caching systems like Redis Cluster use consistent hashing to distribute cached data across multiple cache nodes efficiently.

---

## Q37: What is Service Discovery?
Service discovery is a mechanism in microservices architecture that allows services to dynamically find and communicate with each other without hardcoded network locations.
It helps systems manage changing service instances automatically.

Enables automatic detection and communication between distributed services
Improves scalability and flexibility in dynamic cloud environments
Example: In Kubernetes, services automatically discover other services using internal DNS and service registries.

---

## Q38: What is a Reverse Proxy?
A reverse proxy is a server that receives client requests and forwards them to backend servers on behalf of the clients. it acts as an intermediary between users and application servers.

Improves security, load balancing, caching, and request routing
Hides backend server details and helps distribute incoming traffic efficiently
Example: Nginx works as a reverse proxy by forwarding user requests to multiple application servers behind it.

---

## Q39: What is the difference between ACID and BASE?
ACID	BASE
Focuses on strong consistency and reliability	Focuses on high availability and scalability
Commonly used in relational databases	Commonly used in NoSQL databases
Follows strict transaction rules	Allows eventual consistency
Suitable for critical transactional systems	Suitable for large distributed systems
Prioritizes data accuracy over availability	Prioritizes availability over immediate consistency
Example: Banking systems use ACID databases like PostgreSQL for accurate transactions, while social media platforms use BASE databases like Cassandra for scalability and availability.

---

## Q40: What is the difference between HLD and LLD?
HLD (High-Level Design)	LLD (Low-Level Design)
Focuses on overall system architecture	Focuses on detailed component implementation
Defines modules, databases, APIs, and scalability	Defines classes, methods, and object interactions
Used during system planning phase	Used before actual coding begins
Describes how major components communicate	Describes internal logic of each module
More architecture-oriented	More code-oriented
Example: In a food delivery app, HLD defines services like User Service and Payment Service, while LLD designs classes such as User, Order, and PaymentProcessor.

---

## Q41: What is the difference between Stateful and Stateless Systems?
Stateful System	Stateless System
Stores session or client state on the server	Does not store client state on the server
Each request depends on previous requests	Every request is independent
Harder to scale in distributed systems	Easier to scale and load balance
Requires session management	No session storage required
Better for long user interactions	Better for scalable APIs and microservices
Example: Traditional web login sessions are stateful because the server stores session data, while REST APIs are stateless because each request contains complete authentication information like JWT tokens.

---

## Q42: What is the OSI Model?
The OSI (Open Systems Interconnection) Model is a conceptual framework used to understand how different networking components communicate in a computer network.
It divides network communication into seven layers, where each layer performs a specific function.

Helps standardize network communication and simplifies troubleshooting between systems
Separates networking tasks into layers like Application, Transport, Network, and Physical for better modularity
Example: When a user opens a website, data passes through all OSI layers, from the Application Layer (HTTP request) to the Physical Layer (network transmission).

---

## Q43: What is the TCP/IP Model?
The TCP/IP Model is a networking model used for communication over the internet and modern computer networks.
It defines how data is transmitted between devices using protocols such as TCP, IP, HTTP, and UDP.

Consists of four layers: Application, Transport, Internet, and Network Access Layer
Forms the foundation of internet communication and real-world networking systems
Example: When sending an email, protocols like SMTP use the TCP/IP model to transfer data reliably across networks.

---

## Q44: What is the difference between HTTP and HTTPS?
HTTP	HTTPS
Stands for HyperText Transfer Protocol	Stands for HyperText Transfer Protocol Secure
Data is transferred in plain text	Data is encrypted using SSL/TLS
Less secure for sensitive information	Provides secure communication over the internet
Uses port 80 by default	Uses port 443 by default
Suitable for non-sensitive websites	Used for banking, payments, and secure applications
Example: An online banking website uses HTTPS to encrypt user credentials and payment information during transmission.

---

## Q45: What is the difference between TCP and UDP?
TCP	UDP
Connection-oriented protocol	Connectionless protocol
Provides reliable data delivery	Does not guarantee delivery
Slower due to error checking and acknowledgments	Faster with lower overhead
Used where accuracy is important	Used where speed is more important
Suitable for file transfer and web applications	Suitable for gaming and video streaming
Example: Websites and banking systems use TCP for reliable communication, while online games and live video streaming often use UDP for faster data transfer.

---

## Q46: What is DNS and why is it important?
DNS (Domain Name System) is a system that translates human-readable domain names into IP addresses so computers can locate and communicate with each other over the internet.
It acts like the phonebook of the internet.

Converts domain names like google.com into machine-readable IP addresses
Improves usability by allowing users to access websites using easy-to-remember names instead of numeric IPs
Example: When a user enters "youtube.com" in the browser, DNS converts the domain name into an IP address so the browser can connect to the correct server.

---

## Q47: What happens during a cache miss?
A cache miss occurs when the requested data is not found in the cache memory, forcing the system to fetch the data from the main database or backend service.
After retrieving the data, the system usually stores it in the cache for faster future access.

Increases response time temporarily because the system must access slower backend storage
Frequently accessed data is cached after retrieval to improve future performance and reduce database load
Example: If a user searches for a product that is not available in Redis cache, the application fetches the product details from the database and then stores them in the cache for subsequent requests.

---

## Q48: What is cache invalidation?
Cache invalidation is the process of removing or updating outdated data from the cache to ensure users receive the most recent and correct information.
It helps maintain consistency between cached data and the original data source.

Prevents stale or outdated data from being served to users
Can be performed using techniques like TTL (Time-To-Live), write-through updates, or manual invalidation
Example: In an e-commerce application, when a product price changes in the database, the old cached product information is invalidated or updated so users always see the latest price.

---

## Q49: What happens if the leader node fails in a distributed system?
In a distributed system, if the leader node fails, the remaining nodes detect the failure and elect a new leader to continue coordination and system operations.
This process helps maintain system availability and consistency without manual intervention.

Failure detection is usually performed using heartbeat signals or timeout mechanisms between nodes
A leader election algorithm like Raft or Paxos selects a new leader automatically to restore normal operations
Example: In a distributed database cluster, if the primary server crashes, one of the replica nodes is automatically promoted as the new leader to continue handling write operations.

---

## Q50: How does auto-scaling work in distributed systems?
Auto-scaling is a cloud computing feature that automatically increases or decreases system resources based on traffic, workload, or performance metrics.
It helps maintain application performance while optimizing infrastructure costs.

Automatically adds servers during high traffic and removes unused servers during low traffic periods
Uses monitoring metrics like CPU usage, memory usage, or request count to trigger scaling actions
Example: During a festival sale, an e-commerce platform automatically launches additional application servers to handle increased user traffic and removes extra servers once traffic decreases.

---

## Q51: What is Sticky Session in Load Balancing?
Sticky Session, also known as Session Persistence, is a load balancing technique where requests from the same user are always routed to the same backend server during a session.
It helps maintain user session data without sharing session information across multiple servers.

Ensures user-specific session data remains available on the same server throughout the interaction
Commonly implemented using cookies, client IP addresses, or session identifiers
Example: In an online shopping website, if a user adds items to the cart, sticky sessions ensure subsequent requests from that user continue going to the same server so the cart data remains consistent during checkout.

---

## Q52: How does a load balancer know whether a server is working or failed?
A load balancer regularly checks all servers by sending small test requests called health checks or heartbeat signals.
If a server responds correctly, the load balancer considers it healthy. If the server does not respond, it is marked as failed.

The load balancer keeps checking servers continuously at fixed time intervals.
If the server does not respond or returns errors multiple times, the load balancer marks it as failed and stops sending requests to it.
Example: Imagine a food delivery app running on 4 servers. If one server suddenly crashes, the load balancer detects that the server is not replying to heartbeat checks and immediately stops sending user requests to that server. Users continue using the app normally through the remaining healthy servers.