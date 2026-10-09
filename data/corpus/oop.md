## Q1: What is the difference between Procedural Programming and OOP?
Procedural Programming

Focuses on functions
Data and functions are separate
Less secure
Better for small programs
Example: C

Object-Oriented Programming

Focuses on objects
Data and methods are together inside objects
More secure because of encapsulation
Better for large applications
Example: Java, C++, Python

---

## Q2: What are the advantages and disadvantages of OOPs?
Advantages of OOPs:

Promotes code reusability through inheritance and polymorphism.
Makes code easier to maintain, update, and extend.
Provides better data security using encapsulation and access modifiers.
Improves modularity, making large applications easier to develop and manage.
Reduces code duplication, resulting in cleaner and more organized programs.

Disadvantages of OOPs:

Requires a good understanding of objects and design principles.
Needs proper planning and design before implementation.
Introduces additional complexity for small or simple applications.
Programs may require more memory and execution time due to object creation and abstraction.

---

## Q3: What is a Class?
A class is a building block of Object-Oriented Programs. It is a user-defined data type that contains the data members and member functions that operate on the data members. It is like a blueprint or template of objects having common properties and methods.

---

## Q4: What is an Object?
An object is an instance of a class. Data members and methods of a class cannot be used directly. We need to create an object (or instance) of the class to use them. In simple terms, they are the actual world entities that have a state and behaviour.

```
# class definition
class Student:
    name = ""

# creating object
student1 = Student()
student1.name = "Rahul";

print("student1.name: " + student1.name);
```

Output
student1.name: Rahul

---

## Q5: What are the main features of OOPs?
The main feature of the OOPs, also known as 4 pillars or basic principles of OOPs are as follows:

Encapsulation
Data Abstraction
Polymorphism
Inheritance

---

## Q6: What is Encapsulation?
Encapsulation is the binding of data and methods that manipulate them into a single unit such that the sensitive data is hidden from the users
It is implemented as the processes mentioned below:

Data hiding: A language feature to restrict access to members of an object. For example, private and protected members in C++.
Bundling of data and methods together: Data and methods that operate on that data are bundled together. For example, the data members and member methods that operate on them are wrapped into a single unit known as a class.

---

## Q7: What is Abstraction?
Abstraction is similar to data encapsulation and is very important in OOP. It means showing only the necessary information and hiding the other irrelevant information from the user. Abstraction is implemented using classes and interfaces.

---

## Q8: What is Inheritance? What is its purpose?
The idea of inheritance is simple, a class is derived from another class and uses data and implementation of that other class. The class which is derived is called child or derived or subclass and the class from which the child class is derived is called parent or base or superclass.

The main purpose of Inheritance is to increase code reusability. It is also used to achieve Runtime Polymorphism.

---

## Q9: What is Polymorphism? and types of Polymorphism?
It is the property of some code to behave differently for different contexts. For example, in C++ language, we can define multiple functions having the same name but different working depending on the context.

Polymorphism can be classified into two types based on the time when the call to the object or function is resolved. They are as follows:

Compile Time Polymorphism
Runtime Polymorphism

A) Compile-Time Polymorphism

Compile time polymorphism, also known as static polymorphism or early binding is the type of polymorphism where the binding of the call to its code is done at the compile time. Method overloading or operator overloading are examples of compile-time polymorphism.

B) Runtime Polymorphism

Also known as dynamic polymorphism or late binding, runtime polymorphism is the type of polymorphism where the actual implementation of the function is determined during the runtime or execution. Function overriding is an example of this method.

---

## Q10: What are access specifiers? What is their significance in OOPs?
Access specifiers are special types of keywords that are used to specify or control the accessibility of entities like classes, methods, and so on. Private, Public, and Protected are examples of access specifiers or access modifiers.
The key components of OOPs, encapsulation and data hiding, are largely achieved because of these access specifiers.

---

## Q11: What is the difference between overloading and overriding?
A compile-time polymorphism feature called overloading allows an entity to have numerous implementations of the same name. Method overloading and operator overloading are two examples.

Overriding is a form of runtime polymorphism where an entity with the same name but a different implementation is executed. It is implemented with the help of virtual functions.

---

## Q12: Are there any limitations on Inheritance?
Yes, there are more challenges when you have more authority. Although inheritance is a very strong OOPs feature, it also has significant drawbacks.

As it must pass through several classes to be implemented, inheritance takes longer to process.
The base class and the child class, which are both engaged in inheritance, are also closely related to one another (called tightly coupled). Therefore, if changes need to be made, they may need to be made in both classes at the same time.
Implementing inheritance might be difficult as well. Therefore, if not implemented correctly, this could result in unforeseen mistakes or inaccurate outputs.

---

## Q13: What different types of Inheritance are there?
Inheritance can be classified into 5 types which are as follows:

Single Inheritance: Child class derived directly from the base class
Multiple Inheritance: Child class derived from multiple base classes.
Multilevel Inheritance: Child class derived from the class which is also derived from another base class.
Hierarchical Inheritance: Multiple child classes derived from a single base class.
Hybrid Inheritance: Inheritance consisting of multiple inheritance types of the above specified.

---

## Q14: What is an interface?
A unique class type known as an interface contains methods but not their definitions. Inside an interface, only method declaration is permitted. You cannot make objects using an interface. Instead, you must put that interface into use and specify the procedures for doing so.

---

## Q15: How is an abstract class different from an interface?
An abstract class can have both abstract and concrete methods, whereas an interface mainly defines a contract that classes must implement.
An abstract class can have instance variables and constructors, while an interface can only have constants (public static final) and methods.
A class can extend only one abstract class, but it can implement multiple interfaces.
Use an abstract class when classes share common code, and an interface when unrelated classes need to follow the same contract.

---

## Q16: How much memory does a class occupy?
Classes do not use memory. They merely serve as a template from which items are made. Now, objects actually initialize the class members and methods when they are created, using memory in the process.

---

## Q17: Is it always necessary to create objects from class?
No. If the base class includes non-static methods, an object must be constructed. But no objects need to be generated if the class includes static methods. In this instance, you can use the class name to directly call those static methods.

---

## Q18: What is the difference between a structure and a class in C++?
The structure is also a user-defined datatype in C++ similar to the class with the following differences:

The major difference between a structure and a class is that in a structure, the members are set to public by default while in a class, members are private by default.
The other difference is that we use struct for declaring structure and class for declaring a class in C++.

---

## Q19: What is Constructor?
A constructor is a block of code that initializes the newly created object. A constructor resembles an instance method but it's not a method as it doesn't have a return type. It generally is the method having the same name as the class but in some languages, it might differ. For example:

In python, a constructor is named __init__. 

In C++ and Java, the constructor is named the same as the class name.

---

## Q20: What are the various types of constructors in C++?
The most common classification of constructors includes:

Default Constructor
Non-Parameterized Constructor
Parameterized Constructor
Copy Constructor

1. Default Constructor
The default constructor is a constructor that doesn't take any arguments. It is a non-parameterized constructor that is automatically defined by the compiler when no explicit constructor definition is provided.

It initializes the data members to their default values.

2. Non-Parameterized Constructor
It is a user-defined constructor having no arguments or parameters.

Example:

```
class base:
    def __init__(self):
        
class base:
    def __init__(self):
        print("This is a non-parameterized constructor")
```

3. Parameterized Constructor
The constructors that take some arguments are known as parameterized constructors.

Example:

```
class base:
    def __init__(self, a):
        print("Constructor with argument: {}".format(a))
```

4. Copy Constructor
A copy constructor is a member function that initializes an object using another object of the same class.

Example:

```
class Base:
    def __init__(self, a=0, b=0):
        self.a = a
        self.b = b

    # Copy constructor in Python
    def __copy__(self):
        return Base(self.a, self.b)
```

In Python, we do not have built-in copy constructors like Java and C++ but we can make a workaround using different methods.

---

## Q21: What is a destructor?
A destructor is a method that is automatically called when the object goes out of scope or destroyed.

In C++, the destructor name is also the same as the class name but with the (~) tilde symbol as the prefix.
In Python, the destructor is named __del__.

Example:

```
#include <iostream>
using namespace std;

class base {
public:
    ~base() {
        cout << "This is a destructor";
    }
};
```

In Java, the garbage collector automatically deletes the useless objects so there is no concept of destructor in Java. We could have used finalize() method as a workaround for the java destructor, but it is also deprecated since Java 9.

---

## Q22: Can we overload the constructor in a class?
Yes We can overload the constructor in a class in Java. Constructor Overloading is done when we want constructor with different constructor with different parameter (Number and Type).

---

## Q23: Can we overload the destructor in a class?
No, a destructor cannot be overloaded in a class. There can only be one destructor present in a class.

---

## Q24: What are friend functions and friend classes?
Friend Functions: A friend function is a special function that is allowed to access private and protected data of a class, even though it's not a member of the class.

Friend Class: A friend class is a class that can access the private and protected members of another class. It's like allowing a trusted friend or a group of friends to see and change your personal information, which others cannot.

---

## Q25: What is the virtual function and pure virtual function?
A virtual function is a function that is used to override a method of the parent class in the derived class. It is used to provide abstraction in a class.

In C++ and C#, a virtual function is declared using the virtual keyword,
In Java, every public, non-static, and non-final method is a virtual function.
Python methods are always virtual.

Example:

```
class base:
    def func(self):
        print("This is a virtual function")
```

A pure virtual function, also known as an abstract function, is a member function that doesn't contain any statements. This function is defined in the derived class if needed.

Example:

```
class base {
public:
    virtual void pureVirFunc() = 0;
};
```

In Python, we achieve this using @abstractmethod from the ABC (Abstract Base Class) module.

---

## Q26: What is an abstract class?
In general terms, an abstract class is a class that is intended to be used for inheritance. It cannot be instantiated. An abstract class can consist of both abstract and non-abstract methods.

In C++, an abstract class is a class that contains at least one pure virtual function.
In Java and C#, an abstract class is declared with an abstract keyword.

Example:

```
class absClass {
public:
    virtual void pvFunc() = 0;
};
```

In Python, we use ABC (Abstract Base Class) module to create an abstract class.

---

## Q27: What is the difference between Association, Aggregation, and Composition?
Association, Aggregation, and Composition describe relationships between objects.

Association: A general relationship where two objects are connected but can exist independently.
Aggregation: A weak "has-a" relationship where the child object can exist independently of the parent.
Composition: A strong "has-a" relationship where the child object's lifetime depends on the parent object.
Example: A Student and Teacher have an association, a Department contains Professors (aggregation), and a House consists of Rooms (composition).

---

## Q28: What is the Diamond Problem? How can it be resolved?
The Diamond Problem occurs in multiple inheritance when a class inherits the same base class through two different parent classes, causing ambiguity.

Resolution:

In C++, it is resolved using virtual inheritance. (Solution in C++)
In Java, multiple inheritance of classes is not supported, so the problem is avoided. (Solution in Java)

---

## Q29: What is the difference between shallow copy and deep copy?
A shallow copy copies object references, so both objects share the same nested data. Changes to shared data affect both objects.
A deep copy creates a completely independent copy of the object and all its nested objects. Changes to one object do not affect the other.