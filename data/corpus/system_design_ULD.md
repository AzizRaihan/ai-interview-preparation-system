You're right — numbering them makes it much easier to reference. Here's the full reformatted list with numbers, from 1 to 50, in clean markdown question-answer format.

---

## Q1: What is the purpose of Low-Level System Design in software development?
Low-Level System Design (LLD) is the process of converting a high-level system design into detailed and implementable components that define how the system will actually work at the code level.
It focuses on designing class structures, object relationships, APIs, and internal logic of the system before coding begins.
Removes ambiguity by clearly defining how each module behaves and interacts
Ensures the system is scalable, maintainable, and aligned with the overall architecture
Example: Designing a Parking Lot system where you define classes like Car, ParkingSpot, and ParkingLot, along with their relationships and responsibilities.

---

## Q2: How does database indexing optimize query performance?
Database indexing is a technique used to speed up data retrieval by creating an additional data structure that allows the database to find rows efficiently without scanning the entire table.
It improves query performance by using structures like B-Trees, Hash Indexes, or Bitmap Indexes to quickly locate the required data.
Improves SELECT query performance by enabling fast lookups instead of full table scans
Reduces disk I/O and supports efficient filtering, joins, and range queries
Example: In a user table, creating an index on the user_id column allows the database to directly locate a specific user record without checking every row in the table.

---

## Q3: What are the four pillars of Object-Oriented Programming (OOP)?
The four pillars of OOP are the fundamental concepts used to design modular, reusable, and maintainable object-oriented systems.
These principles help developers organize code efficiently and model real-world entities in software applications.
The four pillars are Encapsulation, Abstraction, Inheritance, and Polymorphism
They improve code reusability, flexibility, security, and maintainability in software systems
Example: In a banking application, inheritance allows different account types to share common features, while polymorphism enables different transaction behaviors using the same method interface.

---

## Q4: Why is concurrency control important in multi-threaded systems?
Concurrency control ensures that multiple threads can safely access and modify shared resources without causing data inconsistency or unexpected behavior.
It prevents issues like race conditions, deadlocks, and corrupted states by managing how threads execute critical sections of code.
Maintains data integrity by controlling simultaneous access to shared resources
Ensures system reliability and correctness under parallel execution
Example: In a banking system, concurrency control ensures that when two users try to withdraw money from the same account at the same time, the balance is updated correctly without losing any transaction.

---

## Q5: What are UML Behavioral Diagrams?
UML Behavioral Diagrams represent the dynamic behavior of a system by showing how objects interact and how the system changes over time in response to events.
They focus on system flow, interactions, and state changes rather than static structure.
Model how different components interact and respond during execution
Help visualize system behavior, workflows, and state transitions clearly
Example: A sequence diagram for a login system shows how the user request flows from UI -> authentication service -> database and back as a response.

---

## Q6: How do you model a sequence diagram for a user login process in UML?
A sequence diagram for login shows how different components interact in a time-ordered flow when a user tries to authenticate into a system.
It captures the sequence of messages exchanged between the user interface, backend services, and database.
Represents interaction flow between User, Login Controller, Authentication Service, and Database
Shows step-by-step message passing for authentication and response generation
Example: User enters credentials -> Login Controller sends request to Authentication Service -> Service verifies data with Database -> Database returns result -> response is sent back to the User (success or failure).

---

## Q7: How would you model the behavior of a system using a state diagram in UML?
A state diagram in UML is used to represent how an object changes its state over time based on different events or conditions.
It defines the lifecycle of an object by showing all possible states and the transitions between them.
Represents object states and transitions triggered by events
Helps model lifecycle behavior of entities like orders, payments, or sessions
Example: In a payment system, the transaction moves through states like Pending -> Processing -> Completed or Failed based on events like payment success or failure.

---

## Q8: What factors influence the choice of appropriate data structures in Low-Level System Design?
The choice of data structures depends on the system requirements such as performance, memory usage, and access patterns.
It is important to select the right structure to ensure efficient operations and scalable system behavior.
Depends on access patterns, time complexity requirements, and memory constraints
Must consider concurrency, scalability, and specific use-case requirements
Example: A caching system typically uses a HashMap for O(1) lookups, while a messaging system uses a Queue to maintain order of message processing.

---

## Q9: When designing a database schema, what are the benefits of normalization?
Normalization is the process of organizing database tables to reduce redundancy and improve data consistency.
It ensures that data is stored in a structured way, making the database more efficient and easier to maintain.
Eliminates data redundancy and avoids duplicate data storage.
Improves data integrity and makes updates, inserts, and deletes more reliable.
Example: Instead of storing customer details in every order record, normalization separates Customers and Orders into different tables, linking them through a customer ID to avoid duplication.

---

## Q10: How do you design an efficient logging and monitoring system for a complex application?
An efficient logging and monitoring system ensures observability of the application by capturing logs, metrics, and alerts in a structured and centralized way.
It helps in debugging issues, tracking performance, and proactively detecting system failures.
Uses structured logging with log levels and centralized log aggregation for better traceability
Implements monitoring dashboards and alerting systems to track metrics like latency, CPU usage, and errors
Example: In a microservices-based system, each service logs events with a correlation ID, which is then used in tools like ELK Stack or Grafana to trace a request end-to-end and monitor performance issues.

---

## Q11: What is tight coupling and why should it be avoided in Low-Level Design?
Tight coupling occurs when classes or modules are highly dependent on each other, making changes difficult and reducing system flexibility.
In LLD, loose coupling is preferred because it improves maintainability, scalability, and testability.
Tight coupling makes code harder to modify, reuse, and unit test
Loose coupling can be achieved using interfaces, abstraction, and dependency injection
Example: If a PaymentService directly creates a PayPal object internally, switching to another payment provider becomes difficult without modifying the service code.

---

## Q12: What are Design Patterns? Explain their importance in software development.
Design patterns are standardized and reusable solutions to common software design problems that occur in object-oriented system design. They provide a proven way to structure code for better design and maintainability.
They are important because they help developers build systems that are cleaner, more flexible, and easier to scale and maintain.
Provide a common design language that improves consistency among developers
Improve maintainability, scalability, and flexibility of software systems
Example: Using the Factory Pattern in a payment system allows the application to create different payment methods (UPI, Card, Wallet) without changing the core business logic.

---

## Q13: Can you explain the Singleton Design Pattern and its use cases?
The Singleton Pattern ensures:
A class has only one instance.
It provides a global access point to that instance.
Implementation (in Java-like pseudocode):

class Singleton { private static Singleton instance; private Singleton() {} // private constructor public static Singleton getInstance() { if (instance == null) { instance = new Singleton(); } return instance; }}
Use Cases:
Database connection pools (only one shared instance).
Configuration managers (centralized global config).
Logging services (consistent, global logging mechanism).
Note: Overuse can introduce global state -> harder to test and maintain.

---

## Q14: What is the Observer Design Pattern? How would you implement it in a real-world scenario?
The Observer Design Pattern is a behavioral design pattern where one object (subject) maintains a list of dependent objects (observers) and automatically notifies them whenever its state changes.
It is used to establish a one-to-many relationship so that multiple objects stay updated without tight coupling.
Defines a one-to-many relationship between a subject and multiple observers
Automatically notifies all observers when the subject's state changes
Example: In a stock market system, when the stock price changes (subject), all registered traders or dashboard applications (observers) are automatically updated with the new price in real time.
Real-world Scenarios:
GUI frameworks: Button (subject) notifies listeners (observers) on click.
Messaging systems: Publisher sends updates -> multiple subscribers receive them.
Stock trading apps: Stock price change (subject) -> all trader dashboards update (observers).
Pseudocode Example:

interface Observer { void update(String msg);}class Subject { List<Observer> observers = new ArrayList<>(); void addObserver(Observer o) { observers.add(o); } void notifyAll(String msg) { for (Observer o : observers) o.update(msg); }}

---

## Q15: Describe the Factory Design Pattern and when you would use it.
The Factory Design Pattern is a creational design pattern that provides a way to create objects without exposing the exact creation logic to the client. Instead, object creation is handled by a factory method or class.
It helps in centralizing object creation and promoting loose coupling between the client and concrete implementations.
Encapsulates object creation logic and hides the instantiation details from the client
Promotes loose coupling and makes the system easier to extend and maintain
Example: In a payment system, a Payment Factory can create different payment objects like UPI, Card, or Wallet based on user input at runtime without the client directly instantiating those classes.
When to Use:
When the type of object isn't known until runtime.
When working with a family of related objects.
To centralize complex creation logic.
Example (Shape Factory):

interface Shape { void draw(); }class Circle implements Shape { public void draw() {...} }class Square implements Shape { public void draw() {...} }class ShapeFactory { public Shape getShape(String type) { if (type.equals("Circle")) return new Circle(); if (type.equals("Square")) return new Square(); return null; }}

---

## Q16: What is the Strategy Design Pattern?
The Strategy Design Pattern is a behavioral design pattern that allows selecting an algorithm or behavior at runtime. Instead of implementing multiple algorithms inside a single class, each algorithm is defined separately and can be swapped dynamically.
It helps in making the system flexible and avoids tightly coupled or hardcoded logic.
Encapsulates different algorithms into separate strategy classes
Allows switching behavior at runtime without modifying existing code
Example: In a payment system, different payment methods like UPI, Credit Card, or PayPal can be implemented as separate strategies, and the system can choose the appropriate one at runtime based on user selection.

---

## Q17: What is the role of interfaces in Low-Level Design?
Interfaces define a contract that classes must follow, helping different components communicate through abstraction instead of direct implementation dependency.
They are widely used in LLD to build flexible and loosely coupled systems.
Interfaces improve extensibility and allow multiple implementations of the same behavior
They support dependency inversion and make unit testing easier using mocks or stubs
Example: A Notification interface can have different implementations such as EmailNotification, SMSNotification, and PushNotification without changing the client code.

---

## Q18: Describe the factors influencing the choice of appropriate algorithms in the design of a sorting system for large datasets.
The choice of sorting algorithm for large datasets depends on system constraints such as data size, memory availability, and performance requirements.
It is important to select an algorithm that balances time efficiency, memory usage, and scalability.
Depends on data size, distribution, memory constraints, and performance requirements
Must consider stability, parallel processing capability, and whether data is in-memory or disk-based
Example: For very large datasets that cannot fit into memory, external merge sort is used, while in-memory systems often prefer MergeSort or QuickSort depending on stability and performance needs.

---

## Q19: In Low-Level System Design, how do you handle versioning and backward compatibility in evolving software systems?
Versioning and backward compatibility ensure that system updates do not break existing clients while allowing the system to evolve safely.
It involves structured API evolution, controlled database changes, and careful rollout strategies.
Uses API versioning and controlled database migrations to manage changes safely
Maintains backward compatibility through gradual deprecation, feature flags, and regression testing
Example: In a REST-based service, /api/v1/users is kept active while /api/v2/users introduces new fields, ensuring older clients continue working without disruption during migration.

---

## Q20: How would you design a secure authentication and authorization system in a distributed application?
A secure authentication and authorization system ensures proper verification of user identity and controlled access to resources across distributed services.
It combines secure identity management, token-based authentication, and fine-grained access control.
Uses secure authentication mechanisms like OAuth 2.0, JWT, MFA, and password hashing for identity verification
Implements authorization using RBAC/ABAC with centralized identity providers and secure token validation across services
Example: In a microservices architecture, a user logs in via an identity provider, receives a JWT token, and each service validates the token before allowing access based on roles such as admin or user.

---

## Q21: Why is modular design important in Low-Level Design?
Modular design divides a system into smaller independent modules, where each module handles a specific responsibility.
This approach improves system maintainability, scalability, and ease of development.
Makes the system easier to debug, test, and extend independently
Reduces code complexity by separating responsibilities into smaller components
Example: In an e-commerce application, separate modules for User Management, Inventory, Payments, and Orders allow teams to work independently without affecting other parts of the system.

---

## Q22: Why is Low-Level Design (LLD) important in software development?
Low-Level Design (LLD) is important because it converts high-level architectural ideas into detailed, implementation-ready modules and components.
It provides a clear structure for developers, reducing confusion during development and improving code quality.
Helps create maintainable, reusable, and scalable code through proper class and module design
Reduces development errors by clearly defining object interactions, APIs, and workflows before coding begins
Example: In a ride-sharing application, LLD defines how modules like Driver, Rider, RideRequest, and Payment interact internally, making implementation easier and more organized for developers.

---

## Q23: Which data structures are commonly used in Low-Level Design (LLD)?
In Low-Level Design, data structures are selected based on how efficiently data needs to be stored, accessed, updated, or processed within the system.
Choosing the right data structure improves application performance, memory usage, and overall code efficiency.
Commonly used data structures include arrays, linked lists, stacks, queues, hash maps, trees, graphs, and heaps
The choice depends on factors like lookup speed, insertion/deletion operations, ordering, and scalability requirements
Example: A messaging application may use queues for message processing, hash maps for quick user lookup, and graphs to represent social connections between users.

---

## Q24: What are the important principles to consider while designing a database?
Database design focuses on organizing data efficiently so that it remains consistent, scalable, and easy to manage as the application grows.
A well-designed database improves query performance, reduces redundancy, and maintains data integrity.
Important principles include normalization, proper relationships, indexing, constraints, and choosing suitable data types
The design should also consider scalability, security, and efficient storage for long-term maintainability
Example: In an e-commerce system, separate tables for users, orders, and products with proper foreign key relationships help maintain organized and consistent data management.

---

## Q25: Explain Object-Oriented Design (OOD) and its importance in software development.
Object-Oriented Design (OOD) is a design approach that models a system using objects, classes, and their interactions to solve real-world problems in a structured way.
It is important because it helps developers build software that is modular, reusable, scalable, and easier to maintain.
Organizes software into classes and objects with clear responsibilities and relationships
Encourages code reusability, flexibility, and easier maintenance through concepts like encapsulation and inheritance
Example: In a banking application, classes such as Account, Customer, and Transaction represent real-world entities and interact with each other to perform operations like deposits and withdrawals.

---

## Q26: What is Dependency Injection and why is it useful in LLD?
Dependency Injection is a design technique where dependencies are provided to a class from outside instead of being created internally by the class itself.
It helps create loosely coupled and easily testable systems.
Improves flexibility by reducing direct dependency between classes
Makes unit testing easier by allowing mock implementations to be injected
Example: Instead of a UserService creating a Database object internally, the database dependency is injected through the constructor, allowing different database implementations to be used easily.

---

## Q27: What are the commonly used UML diagrams in software design?
UML (Unified Modeling Language) diagrams are visual representations used to model the structure and behavior of a software system during the design phase.
They help developers understand system architecture, object interactions, workflows, and component relationships more clearly.
Common UML diagrams include Class Diagrams, Sequence Diagrams, Use Case Diagrams, Activity Diagrams, and State Diagrams
These diagrams help visualize system structure, data flow, object interactions, and user behavior within the application
Example: In a banking system, a Class Diagram may represent entities like Account and Customer, while a Sequence Diagram can illustrate the step-by-step flow of a money transfer process.

---

## Q28: What are code smells and how can they be resolved?
Code smells are indicators of poor design or implementation practices in software code that may not cause immediate bugs but can make the system difficult to maintain, extend, or understand.
They highlight areas where refactoring is needed to improve code quality, readability, and maintainability.
Common code smells include long methods, duplicated code, large classes, tight coupling, and excessive conditional statements
Remedies include refactoring techniques such as modularization, applying design patterns, improving naming conventions, and following SOLID principles
Example: If a single class handles user authentication, payment processing, and notifications together, it becomes a "God Class." This can be resolved by splitting responsibilities into separate classes following the Single Responsibility Principle.

---

## Q29: What are the Types of Design Patterns?
Three main types of Design Patterns are as follows
Creational Patterns: Deal with object creation mechanisms (e.g., Singleton, Factory).
Structural Patterns: Deal with object composition and inheritance (e.g., Adapter, Facade).
Behavioral Patterns: Deal with object interactions and communication (e.g., Observer, Strategy).

---

## Q30: What Are the SOLID Principles?
The SOLID Principles are five design principles developers use to write clean, maintainable, and scalable code:
Single Responsibility Principle (SRP): A class should have a single reason to change.
Open-Closed Principle (OCP): Software entities must be open for extension but closed for modification.
Liskov Substitution Principle (LSP): Objects of a superclass should be replaceable with objects of its subclasses without changing the correctness of the program.
Interface Segregation Principle (ISP): Clients shouldn't be made to depend on interfaces they don't use.
Dependency Inversion Principle (DIP): High-level modules must not be dependent on low-level modules. Both of them must be dependent upon abstractions.

---

## Q31: What is the DRY (Don't Repeat Yourself) principle?
The DRY principle states that duplicate code or logic should be avoided by keeping a single reusable source of truth in the system.
It helps improve maintainability, readability, and consistency in software development.
Reduces code duplication and makes updates easier to manage
Encourages reusable methods, classes, and modular design practices
Example: Instead of writing the same validation logic in multiple classes, a common ValidationService can be created and reused throughout the application.

---

## Q32: When should you avoid using design patterns, and how can you prevent over-engineering?
Design patterns should be avoided when they add unnecessary complexity to a problem that can be solved with a simpler approach. Overusing patterns can lead to rigid, hard-to-maintain code and reduced readability.
Avoid patterns when they introduce unnecessary abstraction or complexity
Use patterns only when there is a clear design problem to solve
Prefer simple solutions first; apply patterns only when needed
Example: Using the Strategy Pattern for tax calculation when there is only one fixed tax rule adds unnecessary classes and complexity. A simple method is sufficient, and the pattern should be introduced only if multiple tax algorithms are needed in the future.

---

## Q33: How do design patterns help in managing dependencies in large-scale applications?
Design patterns help manage dependencies by structuring interactions through abstractions instead of direct class-to-class references.
Reduce tight coupling using interfaces and indirection
Make dependency changes localized and predictable
Example: In a large microservices-based system, Factory and Dependency Injection patterns manage object creation and wiring without spreading dependency logic across the codebase.

---

## Q34: What is the KISS (Keep It Simple, Stupid) principle?
The KISS principle emphasizes designing systems and writing code in the simplest possible way without unnecessary complexity.
Simple designs are easier to understand, debug, maintain, and extend.
Avoids over-engineering and keeps code clean and readable
Improves maintainability by focusing only on required functionality
Example: Using a simple if-else condition for a small business rule is better than introducing multiple complex design patterns unnecessarily.

---

## Q35: What is the YAGNI (You Aren't Gonna Need It) principle?
The YAGNI principle states that developers should implement only the features currently required and avoid building unnecessary functionality in advance.
It helps reduce complexity, development time, and unused code in the system.
Prevents adding features or abstractions that are not immediately needed
Keeps the codebase lightweight, focused, and easier to maintain
Example: Building support for multiple payment gateways when the application currently needs only UPI payments is unnecessary and violates YAGNI.

---

## Q36: When should the Abstract Factory Pattern be preferred over the Factory Method Pattern?
The Abstract Factory Pattern should be preferred when you need to create families of related or dependent objects without specifying their concrete classes.
When multiple related products must be created together and be compatible
When switching entire product families at runtime is required
Example: In a UI toolkit, Abstract Factory can create Windows buttons and menus or Mac buttons and menus together, while Factory Method would handle only one product at a time.

---

## Q37: What are the disadvantages of using the Singleton Pattern?
The Singleton Pattern can introduce hidden design and testing problems despite ensuring a single instance.
Creates global state, making code harder to test and maintain
Introduces tight coupling and limits flexibility
Example: A Singleton database connection can make unit testing difficult because tests cannot easily replace it with a mock or create isolated instances.

---

## Q38: How does the Proxy Pattern differ from the Decorator Pattern?
The Proxy Pattern controls access to an object, while the Decorator Pattern adds new behavior to an object dynamically.
Proxy focuses on access control, lazy loading, or security
Decorator focuses on extending functionality without changing the original class
Example: A Proxy may check user permissions before accessing a file, whereas a Decorator may add logging or compression to file access without restricting it.

---

## Q39: What problem does the Chain of Responsibility Pattern solve?
The Chain of Responsibility Pattern solves the problem of coupling a request sender to a specific request handler by passing the request through a chain of handlers.
Allows multiple objects to handle a request without the sender knowing which one will process it
Promotes loose coupling and flexible request handling
Example: In an approval system, a request passes through manager, director, and CEO handlers until one of them approves it.

---

## Q40: What is the difference between Composition and Aggregation in OOP?
Composition and Aggregation both represent "has-a" relationships between objects, but they differ in ownership and lifecycle dependency.
Composition represents strong ownership, while Aggregation represents a weaker relationship where objects can exist independently.
In Composition, the child object's lifecycle depends on the parent object
In Aggregation, child objects can exist independently even if the parent is destroyed
Example: A House and its Rooms represent Composition because rooms usually do not exist without the house, whereas a Department and Employees represent Aggregation because employees can exist independently of a department.

---

## Q41: Explain how the Command Pattern supports undo and redo functionality.
The Command Pattern encapsulates a request as an object, allowing it to be stored, executed, and reversed later.
Each command stores the information needed to undo an action
Commands can be kept in a history stack for undo and redo
Example: In a text editor, typing or deleting text is stored as command objects, enabling undo and redo by reversing or re-executing those commands.

---

## Q42: What is the difference between Association, Aggregation, and Composition in OOP?
Association, Aggregation, and Composition define relationships between objects in object-oriented design, differing mainly in ownership strength and dependency.
These relationships help model real-world object interactions more clearly in UML and LLD.
Association represents a general relationship, Aggregation shows weak ownership, and Composition shows strong ownership
Composition has the strongest lifecycle dependency, while Association has the loosest relationship
Example: A Teacher teaching Students is an Association, a Department having Employees is Aggregation, and a Car containing an Engine is Composition because the engine is tightly bound to the car's lifecycle.

---

## Q43: Can multiple design patterns be combined in a single solution? Provide examples.
Yes, multiple design patterns are often combined to solve complex design problems more effectively.
Patterns complement each other by addressing different concerns
Improves flexibility, scalability, and maintainability
Example: In an MVC architecture, Observer is used for view updates, Strategy for interchangeable business logic, and Factory for creating objects.

---

## Q44: What factors should be considered before choosing a design pattern?
Choosing a design pattern requires understanding the problem context and long-term impact on the system.
Nature of the problem, complexity, and change frequency
Impact on flexibility, performance, and maintainability
Example: Using Singleton may seem simple for shared configuration, but considering testing and scalability needs might lead to choosing Dependency Injection instead.

---

## Q45: How does the Null Object Pattern help eliminate null checks in code?
The Null Object Pattern replaces null references with a non-functional object that implements the same interface.
Avoids repetitive null checks and conditional logic
Makes code safer and easier to read
Example: Instead of checking if a Logger is null, a NullLogger is used that performs no operation when log() is called.

---

## Q46: What is the difference between static factory methods and the Factory Pattern?
Static factory methods are simple methods that return objects, while the Factory Pattern is a structured design approach for object creation using abstraction.
Static factory methods are tied to a single class and lack polymorphism
Factory Pattern supports extensibility through interfaces and subclasses
Example: A static createUser() method returns a User object directly, whereas a Factory Pattern allows creating different User types without changing client code.

---

## Q47: What is the difference between Abstraction and Encapsulation in OOP?
Abstraction focuses on hiding implementation details and showing only essential functionality, while Encapsulation focuses on restricting direct access to data by wrapping it inside a class.
Both concepts improve code security, maintainability, and modularity in object-oriented systems.
Abstraction hides internal complexity, whereas Encapsulation protects data using access modifiers
Abstraction is achieved using interfaces/abstract classes, while Encapsulation is implemented using private variables and getter-setter methods
Example: A user can drive a car without knowing how the engine works (Abstraction), while the car's engine components remain protected from direct access (Encapsulation).

---

## Q48: How is Inheritance different from Composition in OOP?
Inheritance allows one class to acquire properties and behavior from another class, while Composition builds classes using objects of other classes.
Composition is generally preferred because it provides better flexibility and loose coupling.
Inheritance represents an "is-a" relationship, whereas Composition represents a "has-a" relationship
Composition makes systems easier to modify and maintain compared to deep inheritance hierarchies
Example: A Car "has-an" Engine using Composition, while a Dog "is-an" Animal using Inheritance.

---

## Q49: What is polymorphism in Object-Oriented Programming?
Polymorphism allows the same method or interface to behave differently based on the object or context in which it is used.
It improves flexibility and allows developers to write generic and reusable code.
Compile-time polymorphism is achieved using method overloading, while runtime polymorphism uses method overriding
Helps systems support multiple behaviors through a common interface
Example: A Payment method may behave differently for Credit Card, UPI, or PayPal payments even though all use the same payment() function.

---

## Q50: What is the difference between an Interface and an Abstract Class?
An Interface defines a contract that classes must implement, while an Abstract Class can provide both abstract and partially implemented methods.
Both are used to achieve abstraction but serve different design purposes.
Interfaces support multiple inheritance and define behavior contracts only
Abstract classes are used when classes share common state or partial implementation
Example: A Vehicle interface may define methods like start() and stop(), while an abstract Vehicle class can additionally contain common properties such as speed and fuelType.