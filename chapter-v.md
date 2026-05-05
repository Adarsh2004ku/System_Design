# Chapter V

## Content Page and Index

- [System Design Interviews](#system-design-interviews)
- [URL Shortener](#url-shortener)
- [WhatsApp](#whatsapp)
- [Twitter](#twitter)
- [Netflix](#netflix)
- [Uber](#uber)

---

# System Design Interviews

System design is a very extensive topic and system design interviews are designed to evaluate your capability to produce technical solutions to abstract problems, as such, they're not designed for a specific answer. The unique aspect of system design interviews is the two-way nature between the candidate and the interviewer.

Expectations are quite different at different engineering levels as well. This is because someone with a lot of practical experience will approach it quite differently from someone who's new in the industry. As a result, it's hard to come up with a single strategy that will help us stay organized during the interview.

Let's look at some common strategies for system design interviews:

## Requirements clarifications

System design interview questions, by nature, are vague or abstract. Asking questions about the exact scope of the problem, and clarifying functional requirements early in the interview is essential. Usually, requirements are divided into three parts:

### Functional requirements

These are the requirements that the end user specifically demands as basic functionalities that the system should offer. All these functionalities need to be necessarily incorporated into the system as part of the contract.

For example:

- "What are the features that we need to design for this system?"
- "What are the edge cases we need to consider, if any, in our design?"

### Non-functional requirements

These are the quality constraints that the system must satisfy according to the project contract. The priority or extent to which these factors are implemented varies from one project to another. They are also called non-behavioral requirements. For example, portability, maintainability, reliability, scalability, security, etc.

For example:

- "Each request should be processed with the minimum latency"
- "System should be highly available"

### Extended requirements

These are basically "nice to have" requirements that might be out of the scope of the system.

For example:

- "Our system should record metrics and analytics"
- "Service health and performance monitoring?"

## Estimation and Constraints

Estimate the scale of the system we're going to design. It is important to ask questions such as:

- "What is the desired scale that this system will need to handle?"
- "What is the read/write ratio of our system?"
- "How many requests per second?"
- "How much storage will be needed?"

These questions will help us scale our design later.

## Data model design

Once we have the estimations, we can start with defining the database schema. Doing so in the early stages of the interview would help us to understand the data flow which is the core of every system. In this step, we basically define all the entities and relationships between them.

- "What are the different entities in the system?"
- "What are the relationships between these entities?"
- "How many tables do we need?"
- "Is NoSQL a better choice here?"

## API design

Next, we can start designing APIs for the system. These APIs will help us define the expectations from the system explicitly. We don't have to write any code, just a simple interface defining the API requirements such as parameters, functions, classes, types, entities, etc.

For example:

```tsx
createUser(name: string, email: string): User
```

It is advised to keep the interface as simple as possible and come back to it later when covering extended requirements.

## High-level component design

Now we have established our data model and API design, it's time to identify system components (such as Load Balancers, API Gateway, etc.) that are needed to solve our problem and draft the first design of our system.

- "Is it best to design a monolithic or a microservices architecture?"
- "What type of database should we use?"

Once we have a basic diagram, we can start discussing with the interviewer how the system will work from the client's perspective.

## Detailed design

Now it's time to go into detail about the major components of the system we designed. As always discuss with the interviewer which component may need further improvements.

Here is a good opportunity to demonstrate your experience in the areas of your expertise. Present different approaches, advantages, and disadvantages. Explain your design decisions, and back them up with examples. This is also a good time to discuss any additional features the system might be able to support, though this is optional.

- "How should we partition our data?"
- "What about load distribution?"
- "Should we use cache?"
- "How will we handle a sudden spike in traffic?"

Also, try not to be too opinionated about certain technologies, statements like "I believe that NoSQL databases are just better, SQL databases are not scalable" reflect poorly. As someone who has interviewed a lot of people over the years, my two cents here would be to be humble about what you know and what you do not. Use your existing knowledge with examples to navigate this part of the interview.

## Identify and resolve bottlenecks

Finally, it's time to discuss bottlenecks and approaches to mitigate them. Here are some important questions to ask:

- "Do we have enough database replicas?"
- "Is there any single point of failure?"
- "Is database sharding required?"
- "How can we make our system more robust?"
- "How to improve the availability of our cache?"

Make sure to read the engineering blog of the company you're interviewing with. This will help you get a sense of what technology stack they're using and which problems are important to them.


# URL Shortener

Let's design a URL shortener, similar to services like [Bitly](https://bitly.com), [TinyURL](https://tinyurl.com/app).

## What is a URL Shortener?

A URL shortener service creates an alias or a short URL for a long URL. Users are redirected to the original URL when they visit these short links.

For example, the following long URL can be changed to a shorter URL.

**Long URL**: [https://karanpratapsingh.com/courses/system-design/url-shortener](https://karanpratapsingh.com/courses/system-design/url-shortener)

**Short URL**: [https://bit.ly/3I71d3o](https://bit.ly/3I71d3o)

## Why do we need a URL shortener?

URL shortener saves space in general when we are sharing URLs. Users are also less likely to mistype shorter URLs. Moreover, we can also optimize links across devices, this allows us to track individual links.

## Requirements

Our URL shortening system should meet the following requirements:

### Functional requirements

- Given a URL, our service should generate a _shorter and unique_ alias for it.
- Users should be redirected to the original URL when they visit the short link.
- Links should expire after a default timespan.

### Non-functional requirements

- High availability with minimal latency.
- The system should be scalable and efficient.

### Extended requirements

- Prevent abuse of services.
- Record analytics and metrics for redirections.

## Estimation and Constraints

Let's start with the estimation and constraints.

_Note: Make sure to check any scale or traffic related assumptions with your interviewer._

### Traffic

This will be a read-heavy system, so let's assume a `100:1` read/write ratio with 100 million links generated per month.

**Reads/Writes Per month**

For reads per month:

$$
100 \times 100 \space million = 10 \space billion/month
$$

Similarly for writes:

$$
1 \times 100 \space million = 100 \space million/month
$$

**What would be Requests Per Second (RPS) for our system?**

100 million requests per month translate into 40 requests per second.

$$
\frac{100 \space million}{(30 \space days \times 24 \space hrs \times 3600 \space seconds)} = \sim 40 \space URLs/second
$$

And with a `100:1` read/write ratio, the number of redirections will be:

$$
100 \times 40 \space URLs/second = 4000 \space requests/second
$$

### Bandwidth

Since we expect about 40 URLs every second, and if we assume each request is of size 500 bytes then the total incoming data for write requests would be:

$$
40 \times 500 \space bytes = 20 \space KB/second
$$

Similarly, for the read requests, since we expect about 4K redirections, the total outgoing data would be:

$$
4000 \space URLs/second \times 500 \space bytes = \sim 2 \space MB/second
$$

### Storage

For storage, we will assume we store each link or record in our database for 10 years. Since we expect around 100M new requests every month, the total number of records we will need to store would be:

$$
100 \space million \times 10\space years \times 12 \space months = 12 \space billion
$$

Like earlier, if we assume each stored record will be approximately 500 bytes. We will need around 6TB of storage:

$$
12 \space billion \times 500 \space bytes = 6 \space TB
$$

### Cache

For caching, we will follow the classic [Pareto principle](https://en.wikipedia.org/wiki/Pareto_principle) also known as the 80/20 rule. This means that 80% of the requests are for 20% of the data, so we can cache around 20% of our requests.

Since we get around 4K read or redirection requests each second, this translates into 350M requests per day.

$$
4000 \space URLs/second \times 24 \space hours \times 3600 \space seconds = \sim 350 \space million \space requests/day
$$

Hence, we will need around 35GB of memory per day.

$$
20 \space percent \times 350 \space million \times 500 \space bytes = 35 \space GB/day
$$

### High-level estimate

Here is our high-level estimate:

| Type                 | Estimate   |
| -------------------- | ---------- |
| Writes (New URLs)    | 40/s       |
| Reads (Redirection)  | 4K/s       |
| Bandwidth (Incoming) | 20 KB/s    |
| Bandwidth (Outgoing) | 2 MB/s     |
| Storage (10 years)   | 6 TB       |
| Memory (Caching)     | ~35 GB/day |

## Data model design

Next, we will focus on the data model design. Here is our database schema:

![url-shortener-datamodel](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/url-shortener/url-shortener-datamodel.png)

Initially, we can get started with just two tables:

**users**

Stores user's details such as `name`, `email`, `createdAt`, etc.

**urls**

Contains the new short URL's properties such as `expiration`, `hash`, `originalURL`, and `userID` of the user who created the short URL. We can also use the `hash` column as an [index](https://karanpratapsingh.com/courses/system-design/indexes) to improve the query performance.

### What kind of database should we use?

Since the data is not strongly relational, NoSQL databases such as [Amazon DynamoDB](https://aws.amazon.com/dynamodb), [Apache Cassandra](https://cassandra.apache.org/_/index.html), or [MongoDB](https://www.mongodb.com) will be a better choice here, if we do decide to use an SQL database then we can use something like [Azure SQL Database](https://azure.microsoft.com/en-in/products/azure-sql/database) or [Amazon RDS](https://aws.amazon.com/rds).

_For more details, refer to [SQL vs NoSQL](https://karanpratapsingh.com/courses/system-design/sql-vs-nosql-databases)._

## API design

Let us do a basic API design for our services:

### Create URL

This API should create a new short URL in our system given an original URL.

```tsx
createURL(apiKey: string, originalURL: string, expiration?: Date): string
```

**Parameters**

API Key (`string`): API key provided by the user.

Original URL (`string`): Original URL to be shortened.

Expiration (`Date`): Expiration date of the new URL _(optional)_.

**Returns**

Short URL (`string`): New shortened URL.

### Get URL

This API should retrieve the original URL from a given short URL.

```tsx
getURL(apiKey: string, shortURL: string): string
```

**Parameters**

API Key (`string`): API key provided by the user.

Short URL (`string`): Short URL mapped to the original URL.

**Returns**

Original URL (`string`): Original URL to be retrieved.

### Delete URL

This API should delete a given shortURL from our system.

```tsx
deleteURL(apiKey: string, shortURL: string): boolean
```

**Parameters**

API Key (`string`): API key provided by the user.

Short URL (`string`): Short URL to be deleted.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Why do we need an API key?

As you must've noticed, we're using an API key to prevent abuse of our services. Using this API key we can limit the users to a certain number of requests per second or minute. This is quite a standard practice for developer APIs and should cover our extended requirement.

## High-level design

Now let us do a high-level design of our system.

### URL Encoding

Our system's primary goal is to shorten a given URL, let's look at different approaches:

**Base62 Approach**

In this approach, we can encode the original URL using [Base62](https://en.wikipedia.org/wiki/Base62) which consists of the capital letters A-Z, the lower case letters a-z, and the numbers 0-9.

$$
Number \space of \space URLs = 62^N
$$

Where,

`N`: Number of characters in the generated URL.

So, if we want to generate a URL that is 7 characters long, we will generate ~3.5 trillion different URLs.

$$
\begin{gather*}
62^5 = \sim 916 \space million \space URLs \\
62^6 = \sim 56.8 \space billion \space URLs \\
62^7 = \sim 3.5 \space trillion \space URLs
\end{gather*}
$$

This is the simplest solution here, but it does not guarantee non-duplicate or collision-resistant keys.

**MD5 Approach**

The [MD5 message-digest algorithm](https://en.wikipedia.org/wiki/MD5) is a widely used hash function producing a 128-bit hash value (or 32 hexadecimal digits). We can use these 32 hexadecimal digits for generating 7 characters long URL.

$$
MD5(original\_url) \rightarrow base62encode \rightarrow hash
$$

However, this creates a new issue for us, which is duplication and collision. We can try to re-compute the hash until we find a unique one but that will increase the overhead of our systems. It's better to look for more scalable approaches.

**Counter Approach**

In this approach, we will start with a single server which will maintain the count of the keys generated. Once our service receives a request, it can reach out to the counter which returns a unique number and increments the counter. When the next request comes the counter again returns the unique number and this goes on.

$$
Counter(0-3.5 \space trillion) \rightarrow base62encode \rightarrow hash
$$

The problem with this approach is that it can quickly become a single point for failure. And if we run multiple instances of the counter we can have collision as it's essentially a distributed system.

To solve this issue we can use a distributed system manager such as [Zookeeper](https://zookeeper.apache.org) which can provide distributed synchronization. Zookeeper can maintain multiple ranges for our servers.

$$
\begin{align*}
& Range \space 1: \space 1 \rightarrow 1,000,000 \\
& Range \space 2: \space 1,000,001 \rightarrow 2,000,000 \\
& Range \space 3: \space 2,000,001 \rightarrow 3,000,000 \\
& ...
\end{align*}
$$

Once a server reaches its maximum range Zookeeper will assign an unused counter range to the new server. This approach can guarantee non-duplicate and collision-resistant URLs. Also, we can run multiple instances of Zookeeper to remove the single point of failure.

### Key Generation Service (KGS)

As we discussed, generating a unique key at scale without duplication and collisions can be a bit of a challenge. To solve this problem, we can create a standalone Key Generation Service (KGS) that generates a unique key ahead of time and stores it in a separate database for later use. This approach can make things simple for us.

**How to handle concurrent access?**

Once the key is used, we can mark it in the database to make sure we don't reuse it, however, if there are multiple server instances reading data concurrently, two or more servers might try to use the same key.

The easiest way to solve this would be to store keys in two tables. As soon as a key is used, we move it to a separate table with appropriate locking in place. Also, to improve reads, we can keep some of the keys in memory.

**KGS database estimations**

As per our discussion, we can generate up to ~56.8 billion unique 6 character long keys which will result in us having to store 300 GB of keys.

$$
6 \space characters \times 56.8 \space billion = \sim 390 \space GB
$$

While 390 GB seems like a lot for this simple use case, it is important to remember this is for the entirety of our service lifetime and the size of the keys database would not increase like our main database.

### Caching

Now, let's talk about [caching](https://karanpratapsingh.com/courses/system-design/caching). As per our estimations, we will require around ~35 GB of memory per day to cache 20% of the incoming requests to our services. For this use case, we can use [Redis](https://redis.io) or [Memcached](https://memcached.org) servers alongside our API server.

_For more details, refer to [caching](https://karanpratapsingh.com/courses/system-design/caching)._

### Design

Now that we have identified some core components, let's do the first draft of our system design.

![url-shortener-basic-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/url-shortener/url-shortener-basic-design.png)

Here's how it works:

**Creating a new URL**

1. When a user creates a new URL, our API server requests a new unique key from the Key Generation Service (KGS).
2. Key Generation Service provides a unique key to the API server and marks the key as used.
3. API server writes the new URL entry to the database and cache.
4. Our service returns an HTTP 201 (Created) response to the user.

**Accessing a URL**

1. When a client navigates to a certain short URL, the request is sent to the API servers.
2. The request first hits the cache, and if the entry is not found there then it is retrieved from the database and an HTTP 301 (Redirect) is issued to the original URL.
3. If the key is still not found in the database, an HTTP 404 (Not found) error is sent to the user.

## Detailed design

It's time to discuss the finer details of our design.

### Data Partitioning

To scale out our databases we will need to partition our data. Horizontal partitioning (aka [Sharding](https://karanpratapsingh.com/courses/system-design/sharding)) can be a good first step. We can use partitions schemes such as:

- Hash-Based Partitioning
- List-Based Partitioning
- Range Based Partitioning
- Composite Partitioning

The above approaches can still cause uneven data and load distribution, we can solve this using [Consistent hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing).

_For more details, refer to [Sharding](https://karanpratapsingh.com/courses/system-design/sharding) and [Consistent Hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing)._

### Database cleanup

This is more of a maintenance step for our services and depends on whether we keep the expired entries or remove them. If we do decide to remove expired entries, we can approach this in two different ways:

**Active cleanup**

In active cleanup, we will run a separate cleanup service which will periodically remove expired links from our storage and cache. This will be a very lightweight service like a [cron job](https://en.wikipedia.org/wiki/Cron).

**Passive cleanup**

For passive cleanup, we can remove the entry when a user tries to access an expired link. This can ensure a lazy cleanup of our database and cache.

### Cache

Now let us talk about [caching](https://karanpratapsingh.com/courses/system-design/caching).

**Which cache eviction policy to use?**

As we discussed before, we can use solutions like [Redis](https://redis.io) or [Memcached](https://memcached.org) and cache 20% of the daily traffic but what kind of cache eviction policy would best fit our needs?

[Least Recently Used (LRU)](<https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)>) can be a good policy for our system. In this policy, we discard the least recently used key first.

**How to handle cache miss?**

Whenever there is a cache miss, our servers can hit the database directly and update the cache with the new entries.

### Metrics and Analytics

Recording analytics and metrics is one of our extended requirements. We can store and update metadata like visitor's country, platform, the number of views, etc alongside the URL entry in our database.

### Security

For security, we can introduce private URLs and authorization. A separate table can be used to store user ids that have permission to access a specific URL. If a user does not have proper permissions, we can return an HTTP 401 (Unauthorized) error.

We can also use an [API Gateway](https://karanpratapsingh.com/courses/system-design/api-gateway) as they can support capabilities like authorization, rate limiting, and load balancing out of the box.

## Identify and resolve bottlenecks

![url-shortener-advanced-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/url-shortener/url-shortener-advanced-design.png)

Let us identify and resolve bottlenecks such as single points of failure in our design:

- "What if the API service or Key Generation Service crashes?"
- "How will we distribute our traffic between our components?"
- "How can we reduce the load on our database?"
- "What if the key database used by KGS fails?"
- "How to improve the availability of our cache?"

To make our system more resilient we can do the following:

- Running multiple instances of our Servers and Key Generation Service.
- Introducing [load balancers](https://karanpratapsingh.com/courses/system-design/load-balancing) between clients, servers, databases, and cache servers.
- Using multiple read replicas for our database as it's a read-heavy system.
- Standby replica for our key database in case it fails.
- Multiple instances and replicas for our distributed cache.


# WhatsApp

Let's design a [WhatsApp](https://whatsapp.com) like instant messaging service, similar to services like [Facebook Messenger](https://www.messenger.com), and [WeChat](https://www.wechat.com).

## What is WhatsApp?

WhatsApp is a chat application that provides instant messaging services to its users. It is one of the most used mobile applications on the planet, connecting over 2 billion users in 180+ countries. WhatsApp is also available on the web.

## Requirements

Our system should meet the following requirements:

### Functional requirements

- Should support one-on-one chat.
- Group chats (max 100 people).
- Should support file sharing (image, video, etc.).

### Non-functional requirements

- High availability with minimal latency.
- The system should be scalable and efficient.

### Extended requirements

- Sent, Delivered, and Read receipts of the messages.
- Show the last seen time of users.
- Push notifications.

## Estimation and Constraints

Let's start with the estimation and constraints.

_Note: Make sure to check any scale or traffic-related assumptions with your interviewer._

### Traffic

Let us assume we have 50 million daily active users (DAU) and on average each user sends at least 10 messages to 4 different people every day. This gives us 2 billion messages per day.

$$
50 \space million \times 40 \space messages = 2 \space billion/day
$$

Messages can also contain media such as images, videos, or other files. We can assume that 5 percent of messages are media files shared by the users, which gives us additional 100 million files we would need to store.

$$
5 \space percent \times 2 \space billion = 100 \space million/day
$$

**What would be Requests Per Second (RPS) for our system?**

2 billion requests per day translate into 24K requests per second.

$$
\frac{2 \space billion}{(24 \space hrs \times 3600 \space seconds)} = \sim 24K \space requests/second
$$

### Storage

If we assume each message on average is 100 bytes, we will require about 200 GB of database storage every day.

$$
2 \space billion \times 100 \space bytes = \sim 200 \space GB/day
$$

As per our requirements, we also know that around 5 percent of our daily messages (100 million) are media files. If we assume each file is 100 KB on average, we will require 10 TB of storage every day.

$$
100 \space million \times 100 \space KB = 10 \space TB/day
$$

And for 10 years, we will require about 38 PB of storage.

$$
(10 \space TB + 0.2 \space TB) \times 10 \space years \times 365 \space days = \sim 38 \space PB
$$

### Bandwidth

As our system is handling 10.2 TB of ingress every day, we will require a minimum bandwidth of around 120 MB per second.

$$
\frac{10.2 \space TB}{(24 \space hrs \times 3600 \space seconds)} = \sim 120 \space MB/second
$$

### High-level estimate

Here is our high-level estimate:

| Type                      | Estimate   |
| ------------------------- | ---------- |
| Daily active users (DAU)  | 50 million |
| Requests per second (RPS) | 24K/s      |
| Storage (per day)         | ~10.2 TB   |
| Storage (10 years)        | ~38 PB     |
| Bandwidth                 | ~120 MB/s  |

## Data model design

This is the general data model which reflects our requirements.

![whatsapp-datamodel](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/whatsapp/whatsapp-datamodel.png)

We have the following tables:

**users**

This table will contain a user's information such as `name`, `phoneNumber`, and other details.

**messages**

As the name suggests, this table will store messages with properties such as `type` (text, image, video, etc.), `content`, and timestamps for message delivery. The message will also have a corresponding `chatID` or `groupID`.

**chats**

This table basically represents a private chat between two users and can contain multiple messages.

**users_chats**

This table maps users and chats as multiple users can have multiple chats (N:M relationship) and vice versa.

**groups**

This table represents a group made up of multiple users.

**users_groups**

This table maps users and groups as multiple users can be a part of multiple groups (N:M relationship) and vice versa.

### What kind of database should we use?

While our data model seems quite relational, we don't necessarily need to store everything in a single database, as this can limit our scalability and quickly become a bottleneck.

We will split the data between different services each having ownership over a particular table. Then we can use a relational database such as [PostgreSQL](https://www.postgresql.org) or a distributed NoSQL database such as [Apache Cassandra](https://cassandra.apache.org/_/index.html) for our use case.

## API design

Let us do a basic API design for our services:

### Get all chats or groups

This API will get all chats or groups for a given `userID`.

```tsx
getAll(userID: UUID): Chat[] | Group[]
```

**Parameters**

User ID (`UUID`): ID of the current user.

**Returns**

Result (`Chat[] | Group[]`): All the chats and groups the user is a part of.

### Get messages

Get all messages for a user given the `channelID` (chat or group id).

```tsx
getMessages(userID: UUID, channelID: UUID): Message[]
```

**Parameters**

User ID (`UUID`): ID of the current user.

Channel ID (`UUID`): ID of the channel (chat or group) from which messages need to be retrieved.

**Returns**

Messages (`Message[]`): All the messages in a given chat or group.

### Send message

Send a message from a user to a channel (chat or group).

```tsx
sendMessage(userID: UUID, channelID: UUID, message: Message): boolean
```

**Parameters**

User ID (`UUID`): ID of the current user.

Channel ID (`UUID`): ID of the channel (chat or group) user wants to send a message to.

Message (`Message`): The message (text, image, video, etc.) that the user wants to send.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Join or leave a channel

Allows the user to join or leave a channel (chat or group).

```tsx
joinGroup(userID: UUID, channelID: UUID): boolean
leaveGroup(userID: UUID, channelID: UUID): boolean
```

**Parameters**

User ID (`UUID`): ID of the current user.

Channel ID (`UUID`): ID of the channel (chat or group) the user wants to join or leave.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

## High-level design

Now let us do a high-level design of our system.

### Architecture

We will be using [microservices architecture](https://karanpratapsingh.com/courses/system-design/monoliths-microservices#microservices) since it will make it easier to horizontally scale and decouple our services. Each service will have ownership of its own data model. Let's try to divide our system into some core services.

**User Service**

This is an HTTP-based service that handles user-related concerns such as authentication and user information.

**Chat Service**

The chat service will use WebSockets to establish connections with the client to handle chat and group message-related functionality. We can also use cache to keep track of all the active connections, sort of like sessions which will help us determine if the user is online or not.

**Notification Service**

This service will simply send push notifications to the users. It will be discussed in detail separately.

**Presence Service**

The presence service will keep track of the _last seen_ status of all users. It will be discussed in detail separately.

**Media service**

This service will handle the media (images, videos, files, etc.) uploads. It will be discussed in detail separately.

**What about inter-service communication and service discovery?**

Since our architecture is microservices-based, services will be communicating with each other as well. Generally, REST or HTTP performs well but we can further improve the performance using [gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc#grpc) which is more lightweight and efficient.

[Service discovery](https://karanpratapsingh.com/courses/system-design/service-discovery) is another thing we will have to take into account. We can also use a service mesh that enables managed, observable, and secure communication between individual services.

_Note: Learn more about [REST, GraphQL, gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc) and how they compare with each other._

### Real-time messaging

How do we efficiently send and receive messages? We have two different options:

**Pull model**

The client can periodically send an HTTP request to servers to check if there are any new messages. This can be achieved via something like [Long polling](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#long-polling).

**Push model**

The client opens a long-lived connection with the server and once new data is available it will be pushed to the client. We can use [WebSockets](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#websockets) or [Server-Sent Events (SSE)](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#server-sent-events-sse) for this.

The pull model approach is not scalable as it will create unnecessary request overhead on our servers and most of the time the response will be empty, thus wasting our resources. To minimize latency, using the push model with [WebSockets](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#websockets) is a better choice because then we can push data to the client once it's available without any delay, given that the connection is open with the client. Also, WebSockets provide full-duplex communication, unlike [Server-Sent Events (SSE)](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#server-sent-events-sse) which are only unidirectional.

_Note: Learn more about [Long polling, WebSockets, Server-Sent Events (SSE)](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events)._

### Last seen

To implement the last seen functionality, we can use a [heartbeat](<https://en.wikipedia.org/wiki/Heartbeat_(computing)>) mechanism, where the client can periodically ping the servers indicating its liveness. Since this needs to be as low overhead as possible, we can store the last active timestamp in the cache as follows:

| Key    | Value               |
| ------ | ------------------- |
| User A | 2022-07-01T14:32:50 |
| User B | 2022-07-05T05:10:35 |
| User C | 2022-07-10T04:33:25 |

This will give us the last time the user was active. This functionality will be handled by the presence service combined with [Redis](https://redis.io) or [Memcached](https://memcached.org) as our cache.

Another way to implement this is to track the latest action of the user, once the last activity crosses a certain threshold, such as _"user hasn't performed any action in the last 30 seconds"_, we can show the user as offline and last seen with the last recorded timestamp. This will be more of a lazy update approach and might benefit us over heartbeat mechanism in certain cases.

### Notifications

Once a message is sent in a chat or a group, we will first check if the recipient is active or not, we can get this information by taking the user's active connection and last seen into consideration.

If the recipient is not active, the chat service will add an event to a [message queue](https://karanpratapsingh.com/courses/system-design/message-queues) with additional metadata such as the client's device platform which will be used to route the notification to the correct platform later on.

The notification service will then consume the event from the message queue and forward the request to [Firebase Cloud Messaging (FCM)](https://firebase.google.com/docs/cloud-messaging) or [Apple Push Notification Service (APNS)](https://developer.apple.com/documentation/usernotifications) based on the client's device platform (Android, iOS, web, etc). We can also add support for email and SMS.

**Why are we using a message queue?**

Since most message queues provide best-effort ordering which ensures that messages are generally delivered in the same order as they're sent and that a message is delivered at least once which is an important part of our service functionality.

While this seems like a classic [publish-subscribe](https://karanpratapsingh.com/courses/system-design/publish-subscribe) use case, it is actually not as mobile devices and browsers each have their own way of handling push notifications. Usually, notifications are handled externally via Firebase Cloud Messaging (FCM) or Apple Push Notification Service (APNS) unlike message fan-out which we commonly see in backend services. We can use something like [Amazon SQS](https://aws.amazon.com/sqs) or [RabbitMQ](https://www.rabbitmq.com) to support this functionality.

### Read receipts

Handling read receipts can be tricky, for this use case we can wait for some sort of [Acknowledgment (ACK)](<https://en.wikipedia.org/wiki/Acknowledgement_(data_networks)>) from the client to determine if the message was delivered and update the corresponding `deliveredAt` field. Similarly, we will mark the message as seen once the user opens the chat and update the corresponding `seenAt` timestamp field.

### Design

Now that we have identified some core components, let's do the first draft of our system design.

![whatsapp-basic-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/whatsapp/whatsapp-basic-design.png)

## Detailed design

It's time to discuss our design decisions in detail.

### Data Partitioning

To scale out our databases we will need to partition our data. Horizontal partitioning (aka [Sharding](https://karanpratapsingh.com/courses/system-design/sharding)) can be a good first step. We can use partitions schemes such as:

- Hash-Based Partitioning
- List-Based Partitioning
- Range Based Partitioning
- Composite Partitioning

The above approaches can still cause uneven data and load distribution, we can solve this using [Consistent hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing).

_For more details, refer to [Sharding](https://karanpratapsingh.com/courses/system-design/sharding) and [Consistent Hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing)._

### Caching

In a messaging application, we have to be careful about using cache as our users expect the latest data, but many users will be requesting the same messages, especially in a group chat. So, to prevent usage spikes from our resources we can cache older messages.

Some group chats can have thousands of messages and sending that over the network will be really inefficient, to improve efficiency we can add pagination to our system APIs. This decision will be helpful for users with limited network bandwidth as they won't have to retrieve old messages unless requested.

**Which cache eviction policy to use?**

We can use solutions like [Redis](https://redis.io) or [Memcached](https://memcached.org) and cache 20% of the daily traffic but what kind of cache eviction policy would best fit our needs?

[Least Recently Used (LRU)](<https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)>) can be a good policy for our system. In this policy, we discard the least recently used key first.

**How to handle cache miss?**

Whenever there is a cache miss, our servers can hit the database directly and update the cache with the new entries.

_For more details, refer to [Caching](https://karanpratapsingh.com/courses/system-design/caching)._

### Media access and storage

As we know, most of our storage space will be used for storing media files such as images, videos, or other files. Our media service will be handling both access and storage of the user media files.

But where can we store files at scale? Well, [object storage](https://karanpratapsingh.com/courses/system-design/storage#object-storage) is what we're looking for. Object stores break data files up into pieces called objects. It then stores those objects in a single repository, which can be spread out across multiple networked systems. We can also use distributed file storage such as [HDFS](https://karanpratapsingh.com/courses/system-design/storage#hdfs) or [GlusterFS](https://www.gluster.org).

_Fun fact: WhatsApp deletes media on its servers once it has been downloaded by the user._

We can use object stores like [Amazon S3](https://aws.amazon.com/s3), [Azure Blob Storage](https://azure.microsoft.com/en-in/services/storage/blobs), or [Google Cloud Storage](https://cloud.google.com/storage) for this use case.

### Content Delivery Network (CDN)

[Content Delivery Network (CDN)](https://karanpratapsingh.com/courses/system-design/content-delivery-network) increases content availability and redundancy while reducing bandwidth costs. Generally, static files such as images, and videos are served from CDN. We can use services like [Amazon CloudFront](https://aws.amazon.com/cloudfront) or [Cloudflare CDN](https://www.cloudflare.com/cdn) for this use case.

### API gateway

Since we will be using multiple protocols like HTTP, WebSocket, TCP/IP, deploying multiple L4 (transport layer) or L7 (application layer) type load balancers separately for each protocol will be expensive. Instead, we can use an [API Gateway](https://karanpratapsingh.com/courses/system-design/api-gateway) that supports multiple protocols without any issues.

API Gateway can also offer other features such as authentication, authorization, rate limiting, throttling, and API versioning which will improve the quality of our services.

We can use services like [Amazon API Gateway](https://aws.amazon.com/api-gateway) or [Azure API Gateway](https://azure.microsoft.com/en-in/services/api-management) for this use case.

## Identify and resolve bottlenecks

![whatsapp-advanced-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/whatsapp/whatsapp-advanced-design.png)

Let us identify and resolve bottlenecks such as single points of failure in our design:

- "What if one of our services crashes?"
- "How will we distribute our traffic between our components?"
- "How can we reduce the load on our database?"
- "How to improve the availability of our cache?"
- "Wouldn't API Gateway be a single point of failure?"
- "How can we make our notification system more robust?"
- "How can we reduce media storage costs"?
- "Does chat service has too much responsibility?"

To make our system more resilient we can do the following:

- Running multiple instances of each of our services.
- Introducing [load balancers](https://karanpratapsingh.com/courses/system-design/load-balancing) between clients, servers, databases, and cache servers.
- Using multiple read replicas for our databases.
- Multiple instances and replicas for our distributed cache.
- We can have a standby replica of our API Gateway.
- Exactly once delivery and message ordering is challenging in a distributed system, we can use a dedicated [message broker](https://karanpratapsingh.com/courses/system-design/message-brokers) such as [Apache Kafka](https://kafka.apache.org) or [NATS](https://nats.io) to make our notification system more robust.
- We can add media processing and compression capabilities to the media service to compress large files similar to WhatsApp which will save a lot of storage space and reduce cost.
- We can create a group service separate from the chat service to further decouple our services.


# Twitter

Let's design a [Twitter](https://twitter.com) like social media service, similar to services like [Facebook](https://facebook.com), [Instagram](https://instagram.com), etc.

## What is Twitter?

Twitter is a social media service where users can read or post short messages (up to 280 characters) called tweets. It is available on the web and mobile platforms such as Android and iOS.

## Requirements

Our system should meet the following requirements:

### Functional requirements

- Should be able to post new tweets (can be text, image, video, etc.).
- Should be able to follow other users.
- Should have a newsfeed feature consisting of tweets from the people the user is following.
- Should be able to search tweets.

### Non-Functional requirements

- High availability with minimal latency.
- The system should be scalable and efficient.

### Extended requirements

- Metrics and analytics.
- Retweet functionality.
- Favorite tweets.

## Estimation and Constraints

Let's start with the estimation and constraints.

_Note: Make sure to check any scale or traffic-related assumptions with your interviewer._

### Traffic

This will be a read-heavy system, let us assume we have 1 billion total users with 200 million daily active users (DAU), and on average each user tweets 5 times a day. This gives us 1 billion tweets per day.

$$
200 \space million \times 5 \space tweets = 1 \space billion/day
$$

Tweets can also contain media such as images, or videos. We can assume that 10 percent of tweets are media files shared by the users, which gives us additional 100 million files we would need to store.

$$
10 \space percent \times 1 \space billion = 100 \space million/day
$$

**What would be Requests Per Second (RPS) for our system?**

1 billion requests per day translate into 12K requests per second.

$$
\frac{1 \space billion}{(24 \space hrs \times 3600 \space seconds)} = \sim 12K \space requests/second
$$

### Storage

If we assume each message on average is 100 bytes, we will require about 100 GB of database storage every day.

$$
1 \space billion \times 100 \space bytes = \sim 100 \space GB/day
$$

We also know that around 10 percent of our daily messages (100 million) are media files per our requirements. If we assume each file is 50 KB on average, we will require 5 TB of storage every day.

$$
100 \space million \times 50 \space KB = 5 \space TB/day
$$

And for 10 years, we will require about 19 PB of storage.

$$
(5 \space TB + 0.1 \space TB) \times 365 \space days \times 10 \space years = \sim 19 \space PB
$$

### Bandwidth

As our system is handling 5.1 TB of ingress every day, we will require a minimum bandwidth of around 60 MB per second.

$$
\frac{5.1 \space TB}{(24 \space hrs \times 3600 \space seconds)} = \sim 60 \space MB/second
$$

### High-level estimate

Here is our high-level estimate:

| Type                      | Estimate    |
| ------------------------- | ----------- |
| Daily active users (DAU)  | 100 million |
| Requests per second (RPS) | 12K/s       |
| Storage (per day)         | ~5.1 TB     |
| Storage (10 years)        | ~19 PB      |
| Bandwidth                 | ~60 MB/s    |

## Data model design

This is the general data model which reflects our requirements.

![twitter-datamodel](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/twitter/twitter-datamodel.png)

We have the following tables:

**users**

This table will contain a user's information such as `name`, `email`, `dob`, and other details.

**tweets**

As the name suggests, this table will store tweets and their properties such as `type` (text, image, video, etc.), `content`, etc. We will also store the corresponding `userID`.

**favorites**

This table maps tweets with users for the favorite tweets functionality in our application.

**followers**

This table maps the followers and [followees](https://en.wiktionary.org/wiki/followee) as users can follow each other (N:M relationship).

**feeds**

This table stores feed properties with the corresponding `userID`.

**feeds_tweets**

This table maps tweets and feed (N:M relationship).

### What kind of database should we use?

While our data model seems quite relational, we don't necessarily need to store everything in a single database, as this can limit our scalability and quickly become a bottleneck.

We will split the data between different services each having ownership over a particular table. Then we can use a relational database such as [PostgreSQL](https://www.postgresql.org) or a distributed NoSQL database such as [Apache Cassandra](https://cassandra.apache.org/_/index.html) for our use case.

## API design

Let us do a basic API design for our services:

### Post a tweet

This API will allow the user to post a tweet on the platform.

```tsx
postTweet(userID: UUID, content: string, mediaURL?: string): boolean
```

**Parameters**

User ID (`UUID`): ID of the user.

Content (`string`): Contents of the tweet.

Media URL (`string`): URL of the attached media _(optional)_.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Follow or unfollow a user

This API will allow the user to follow or unfollow another user.

```tsx
follow(followerID: UUID, followeeID: UUID): boolean
unfollow(followerID: UUID, followeeID: UUID): boolean
```

**Parameters**

Follower ID (`UUID`): ID of the current user.

Followee ID (`UUID`): ID of the user we want to follow or unfollow.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Get newsfeed

This API will return all the tweets to be shown within a given newsfeed.

```tsx
getNewsfeed(userID: UUID): Tweet[]
```

**Parameters**

User ID (`UUID`): ID of the user.

**Returns**

Tweets (`Tweet[]`): All the tweets to be shown within a given newsfeed.

## High-level design

Now let us do a high-level design of our system.

### Architecture

We will be using [microservices architecture](https://karanpratapsingh.com/courses/system-design/monoliths-microservices#microservices) since it will make it easier to horizontally scale and decouple our services. Each service will have ownership of its own data model. Let's try to divide our system into some core services.

**User Service**

This service handles user-related concerns such as authentication and user information.

**Newsfeed Service**

This service will handle the generation and publishing of user newsfeeds. It will be discussed in detail separately.

**Tweet Service**

The tweet service will handle tweet-related use cases such as posting a tweet, favorites, etc.

**Search Service**

The service is responsible for handling search-related functionality. It will be discussed in detail separately.

**Media service**

This service will handle the media (images, videos, files, etc.) uploads. It will be discussed in detail separately.

**Notification Service**

This service will simply send push notifications to the users.

**Analytics Service**

This service will be used for metrics and analytics use cases.

**What about inter-service communication and service discovery?**

Since our architecture is microservices-based, services will be communicating with each other as well. Generally, REST or HTTP performs well but we can further improve the performance using [gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc#grpc) which is more lightweight and efficient.

[Service discovery](https://karanpratapsingh.com/courses/system-design/service-discovery) is another thing we will have to take into account. We can also use a service mesh that enables managed, observable, and secure communication between individual services.

_Note: Learn more about [REST, GraphQL, gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc) and how they compare with each other._

### Newsfeed

When it comes to the newsfeed, it seems easy enough to implement, but there are a lot of things that can make or break this feature. So, let's divide our problem into two parts:

**Generation**

Let's assume we want to generate the feed for user A, we will perform the following steps:

1. Retrieve the IDs of all the users and entities (hashtags, topics, etc.) user A follows.
2. Fetch the relevant tweets for each of the retrieved IDs.
3. Use a ranking algorithm to rank the tweets based on parameters such as relevance, time, engagement, etc.
4. Return the ranked tweets data to the client in a paginated manner.

Feed generation is an intensive process and can take quite a lot of time, especially for users following a lot of people. To improve the performance, the feed can be pre-generated and stored in the cache, then we can have a mechanism to periodically update the feed and apply our ranking algorithm to the new tweets.

**Publishing**

Publishing is the step where the feed data is pushed according to each specific user. This can be a quite heavy operation, as a user may have millions of friends or followers. To deal with this, we have three different approaches:

- Pull Model (or Fan-out on load)

![newsfeed-pull-model](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/twitter/newsfeed-pull-model.png)

When a user creates a tweet, and a follower reloads their newsfeed, the feed is created and stored in memory. The most recent feed is only loaded when the user requests it. This approach reduces the number of write operations on our database.

The downside of this approach is that the users will not be able to view recent feeds unless they "pull" the data from the server, which will increase the number of read operations on the server.

- Push Model (or Fan-out on write)

![newsfeed-push-model](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/twitter/newsfeed-push-model.png)

In this model, once a user creates a tweet, it is "pushed" to all the follower's feeds immediately. This prevents the system from having to go through a user's entire followers list to check for updates.

However, the downside of this approach is that it would increase the number of write operations on the database.

- Hybrid Model

A third approach is a hybrid model between the pull and push model. It combines the beneficial features of the above two models and tries to provide a balanced approach between the two.

The hybrid model allows only users with a lesser number of followers to use the push model. For users with a higher number of followers such as celebrities, the pull model is used.

### Ranking Algorithm

As we discussed, we will need a ranking algorithm to rank each tweet according to its relevance to each specific user.

For example, Facebook used to utilize an [EdgeRank](https://en.wikipedia.org/wiki/EdgeRank) algorithm. Here, the rank of each feed item is described by:

$$
Rank = Affinity \times Weight \times Decay
$$

Where,

`Affinity`: is the "closeness" of the user to the creator of the edge. If a user frequently likes, comments, or messages the edge creator, then the value of affinity will be higher, resulting in a higher rank for the post.

`Weight`: is the value assigned according to each edge. A comment can have a higher weightage than likes, and thus a post with more comments is more likely to get a higher rank.

`Decay`: is the measure of the creation of the edge. The older the edge, the lesser will be the value of decay and eventually the rank.

Nowadays, algorithms are much more complex and ranking is done using machine learning models which can take thousands of factors into consideration.

### Retweets

Retweets are one of our extended requirements. To implement this feature, we can simply create a new tweet with the user id of the user retweeting the original tweet and then modify the `type` enum and `content` property of the new tweet to link it with the original tweet.

For example, the `type` enum property can be of type tweet, similar to text, video, etc and `content` can be the id of the original tweet. Here the first row indicates the original tweet while the second row is how we can represent a retweet.

| id                  | userID              | type  | content                      | createdAt     |
| ------------------- | ------------------- | ----- | ---------------------------- | ------------- |
| ad34-291a-45f6-b36c | 7a2c-62c4-4dc8-b1bb | text  | Hey, this is my first tweet… | 1658905644054 |
| f064-49ad-9aa2-84a6 | 6aa2-2bc9-4331-879f | tweet | ad34-291a-45f6-b36c          | 1658906165427 |

This is a very basic implementation. To improve this we can create a separate table itself to store retweets.

### Search

Sometimes traditional DBMS are not performant enough, we need something which allows us to store, search, and analyze huge volumes of data quickly and in near real-time and give results within milliseconds. [Elasticsearch](https://www.elastic.co) can help us with this use case.

[Elasticsearch](https://www.elastic.co) is a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured. It is built on top of [Apache Lucene](https://lucene.apache.org).

**How do we identify trending topics?**

Trending functionality will be based on top of the search functionality. We can cache the most frequently searched queries, hashtags, and topics in the last `N` seconds and update them every `M` seconds using some sort of batch job mechanism. Our ranking algorithm can also be applied to the trending topics to give them more weight and personalize them for the user.

### Notifications

Push notifications are an integral part of any social media platform. We can use a message queue or a message broker such as [Apache Kafka](https://kafka.apache.org) with the notification service to dispatch requests to [Firebase Cloud Messaging (FCM)](https://firebase.google.com/docs/cloud-messaging) or [Apple Push Notification Service (APNS)](https://developer.apple.com/documentation/usernotifications) which will handle the delivery of the push notifications to user devices.

_For more details, refer to the [WhatsApp](https://karanpratapsingh.com/courses/system-design/whatsapp#notifications) system design where we discuss push notifications in detail._

## Detailed design

It's time to discuss our design decisions in detail.

### Data Partitioning

To scale out our databases we will need to partition our data. Horizontal partitioning (aka [Sharding](https://karanpratapsingh.com/courses/system-design/sharding)) can be a good first step. We can use partitions schemes such as:

- Hash-Based Partitioning
- List-Based Partitioning
- Range Based Partitioning
- Composite Partitioning

The above approaches can still cause uneven data and load distribution, we can solve this using [Consistent hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing).

_For more details, refer to [Sharding](https://karanpratapsingh.com/courses/system-design/sharding) and [Consistent Hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing)._

### Mutual friends

For mutual friends, we can build a social graph for every user. Each node in the graph will represent a user and a directional edge will represent followers and followees. After that, we can traverse the followers of a user to find and suggest a mutual friend. This would require a graph database such as [Neo4j](https://neo4j.com) or [ArangoDB](https://www.arangodb.com).

This is a pretty simple algorithm, to improve our suggestion accuracy, we will need to incorporate a recommendation model which uses machine learning as part of our algorithm.

### Metrics and Analytics

Recording analytics and metrics is one of our extended requirements. As we will be using [Apache Kafka](https://kafka.apache.org) to publish all sorts of events, we can process these events and run analytics on the data using [Apache Spark](https://spark.apache.org) which is an open-source unified analytics engine for large-scale data processing.

### Caching

In a social media application, we have to be careful about using cache as our users expect the latest data. So, to prevent usage spikes from our resources we can cache the top 20% of the tweets.

To further improve efficiency we can add pagination to our system APIs. This decision will be helpful for users with limited network bandwidth as they won't have to retrieve old messages unless requested.

**Which cache eviction policy to use?**

We can use solutions like [Redis](https://redis.io) or [Memcached](https://memcached.org) and cache 20% of the daily traffic but what kind of cache eviction policy would best fit our needs?

[Least Recently Used (LRU)](<https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)>) can be a good policy for our system. In this policy, we discard the least recently used key first.

**How to handle cache miss?**

Whenever there is a cache miss, our servers can hit the database directly and update the cache with the new entries.

_For more details, refer to [Caching](https://karanpratapsingh.com/courses/system-design/caching)._

### Media access and storage

As we know, most of our storage space will be used for storing media files such as images, videos, or other files. Our media service will be handling both access and storage of the user media files.

But where can we store files at scale? Well, [object storage](https://karanpratapsingh.com/courses/system-design/storage#object-storage) is what we're looking for. Object stores break data files up into pieces called objects. It then stores those objects in a single repository, which can be spread out across multiple networked systems. We can also use distributed file storage such as [HDFS](https://karanpratapsingh.com/courses/system-design/storage#hdfs) or [GlusterFS](https://www.gluster.org).

### Content Delivery Network (CDN)

[Content Delivery Network (CDN)](https://karanpratapsingh.com/courses/system-design/content-delivery-network) increases content availability and redundancy while reducing bandwidth costs. Generally, static files such as images, and videos are served from CDN. We can use services like [Amazon CloudFront](https://aws.amazon.com/cloudfront) or [Cloudflare CDN](https://www.cloudflare.com/cdn) for this use case.

## Identify and resolve bottlenecks

![twitter-advanced-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/twitter/twitter-advanced-design.png)

Let us identify and resolve bottlenecks such as single points of failure in our design:

- "What if one of our services crashes?"
- "How will we distribute our traffic between our components?"
- "How can we reduce the load on our database?"
- "How to improve the availability of our cache?"
- "How can we make our notification system more robust?"
- "How can we reduce media storage costs"?

To make our system more resilient we can do the following:

- Running multiple instances of each of our services.
- Introducing [load balancers](https://karanpratapsingh.com/courses/system-design/load-balancing) between clients, servers, databases, and cache servers.
- Using multiple read replicas for our databases.
- Multiple instances and replicas for our distributed cache.
- Exactly once delivery and message ordering is challenging in a distributed system, we can use a dedicated [message broker](https://karanpratapsingh.com/courses/system-design/message-brokers) such as [Apache Kafka](https://kafka.apache.org) or [NATS](https://nats.io) to make our notification system more robust.
- We can add media processing and compression capabilities to the media service to compress large files which will save a lot of storage space and reduce cost.


# Netflix

Let's design a [Netflix](https://netflix.com) like video streaming service, similar to services like [Amazon Prime Video](https://www.primevideo.com), [Disney Plus](https://www.disneyplus.com), [Hulu](https://www.hulu.com), [Youtube](https://youtube.com), [Vimeo](https://vimeo.com), etc.

## What is Netflix?

Netflix is a subscription-based streaming service that allows its members to watch TV shows and movies on an internet-connected device. It is available on platforms such as the Web, iOS, Android, TV, etc.

## Requirements

Our system should meet the following requirements:

### Functional requirements

- Users should be able to stream and share videos.
- The content team (or users in YouTube's case) should be able to upload new videos (movies, tv shows episodes, and other content).
- Users should be able to search for videos using titles or tags.
- Users should be able to comment on a video similar to YouTube.

### Non-Functional requirements

- High availability with minimal latency.
- High reliability, no uploads should be lost.
- The system should be scalable and efficient.

### Extended requirements

- Certain content should be [geo-blocked](https://en.wikipedia.org/wiki/Geo-blocking).
- Resume video playback from the point user left off.
- Record metrics and analytics of videos.

## Estimation and Constraints

Let's start with the estimation and constraints.

_Note: Make sure to check any scale or traffic-related assumptions with your interviewer._

### Traffic

This will be a read-heavy system, let us assume we have 1 billion total users with 200 million daily active users (DAU), and on average each user watches 5 videos a day. This gives us 1 billion videos watched per day.

$$
200 \space million \times 5 \space videos = 1 \space billion/day
$$

Assuming a `200:1` read/write ratio, about 5 million videos will be uploaded every day.

$$
\frac{1}{200} \times 1 \space billion = 5 \space million/day
$$

**What would be Requests Per Second (RPS) for our system?**

1 billion requests per day translate into 12K requests per second.

$$
\frac{1 \space billion}{(24 \space hrs \times 3600 \space seconds)} = \sim 12K \space requests/second
$$

### Storage

If we assume each video is 100 MB on average, we will require about 500 TB of storage every day.

$$
5 \space million \times 100 \space MB = 500 \space TB/day
$$

And for 10 years, we will require an astounding 1,825 PB of storage.

$$
500 \space TB \times 365 \space days \times 10 \space years = \sim 1,825 \space PB
$$

### Bandwidth

As our system is handling 500 TB of ingress every day, we will require a minimum bandwidth of around 5.8 GB per second.

$$
\frac{500 \space TB}{(24 \space hrs \times 3600 \space seconds)} = \sim 5.8 \space GB/second
$$

### High-level estimate

Here is our high-level estimate:

| Type                      | Estimate    |
| ------------------------- | ----------- |
| Daily active users (DAU)  | 200 million |
| Requests per second (RPS) | 12K/s       |
| Storage (per day)         | ~500 TB     |
| Storage (10 years)        | ~1,825 PB   |
| Bandwidth                 | ~5.8 GB/s   |

## Data model design

This is the general data model which reflects our requirements.

![netflix-datamodel](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/netflix/netflix-datamodel.png)

We have the following tables:

**users**

This table will contain a user's information such as `name`, `email`, `dob`, and other details.

**videos**

As the name suggests, this table will store videos and their properties such as `title`, `streamURL`, `tags`, etc. We will also store the corresponding `userID`.

**tags**

This table will simply store tags associated with a video.

**views**

This table helps us to store all the views received on a video.

**comments**

This table stores all the comments received on a video (like YouTube).

### What kind of database should we use?

While our data model seems quite relational, we don't necessarily need to store everything in a single database, as this can limit our scalability and quickly become a bottleneck.

We will split the data between different services each having ownership over a particular table. Then we can use a relational database such as [PostgreSQL](https://www.postgresql.org) or a distributed NoSQL database such as [Apache Cassandra](https://cassandra.apache.org/_/index.html) for our use case.

## API design

Let us do a basic API design for our services:

### Upload a video

Given a byte stream, this API enables video to be uploaded to our service.

```tsx
uploadVideo(title: string, description: string, data: Stream<byte>, tags?: string[]): boolean
```

**Parameters**

Title (`string`): Title of the new video.

Description (`string`): Description of the new video.

Data (`byte[]`): Byte stream of the video data.

Tags (`string[]`): Tags for the video _(optional)_.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Streaming a video

This API allows our users to stream a video with the preferred codec and resolution.

```tsx
streamVideo(videoID: UUID, codec: Enum<string>, resolution: Tuple<int>, offset?: int): VideoStream
```

**Parameters**

Video ID (`UUID`): ID of the video that needs to be streamed.

Codec (`Enum<string>`): Required [codec](https://en.wikipedia.org/wiki/Video_codec) of the requested video, such as `h.265`, `h.264`, `VP9`, etc.

Resolution (`Tuple<int>`): [Resolution](https://en.wikipedia.org/wiki/Display_resolution) of the requested video.

Offset (`int`): Offset of the video stream in seconds to stream data from any point in the video _(optional)_.

**Returns**

Stream (`VideoStream`): Data stream of the requested video.

### Search for a video

This API will enable our users to search for a video based on its title or tags.

```tsx
searchVideo(query: string, nextPage?: string): Video[]
```

**Parameters**

Query (`string`): Search query from the user.

Next Page (`string`): Token for the next page, this can be used for pagination _(optional)_.

**Returns**

Videos (`Video[]`): All the videos available for a particular search query.

### Add a comment

This API will allow our users to post a comment on a video (like YouTube).

```tsx
comment(videoID: UUID, comment: string): boolean
```

**Parameters**

VideoID (`UUID`): ID of the video user wants to comment on.

Comment (`string`): The text content of the comment.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

## High-level design

Now let us do a high-level design of our system.

### Architecture

We will be using [microservices architecture](https://karanpratapsingh.com/courses/system-design/monoliths-microservices#microservices) since it will make it easier to horizontally scale and decouple our services. Each service will have ownership of its own data model. Let's try to divide our system into some core services.

**User Service**

This service handles user-related concerns such as authentication and user information.

**Stream Service**

The stream service will handle video streaming-related functionality.

**Search Service**

The service is responsible for handling search-related functionality. It will be discussed in detail separately.

**Media service**

This service will handle the video uploads and processing. It will be discussed in detail separately.

**Analytics Service**

This service will be used for metrics and analytics use cases.

**What about inter-service communication and service discovery?**

Since our architecture is microservices-based, services will be communicating with each other as well. Generally, REST or HTTP performs well but we can further improve the performance using [gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc#grpc) which is more lightweight and efficient.

[Service discovery](https://karanpratapsingh.com/courses/system-design/service-discovery) is another thing we will have to take into account. We can also use a service mesh that enables managed, observable, and secure communication between individual services.

_Note: Learn more about [REST, GraphQL, gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc) and how they compare with each other._

### Video processing

![video-processing-pipeline](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/netflix/video-processing-pipeline.png)

There are so many variables in play when it comes to processing a video. For example, an average data size of two-hour raw 8K footage from a high-end camera can easily be up to 4 TB, thus we need to have some kind of processing to reduce both storage and delivery costs.

Here's how we can process videos once they're uploaded by the content team (or users in YouTube's case) and are queued for processing in our [message queue](https://karanpratapsingh.com/courses/system-design/message-queues).

Let's discuss how this works:

- **File Chunker**

![file-chunking](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/netflix/file-chunking.png)

This is the first step of our processing pipeline. File chunking is the process of splitting a file into smaller pieces called chunks. It can help us eliminate duplicate copies of repeating data on storage, and reduces the amount of data sent over the network by only selecting changed chunks.

Usually, a video file can be split into equal size chunks based on timestamps but Netflix instead splits chunks based on scenes. This slight variation becomes a huge factor for a better user experience since whenever the client requests a chunk from the server, there is a lower chance of interruption as a complete scene will be retrieved.

- **Content Filter**

This step checks if the video adheres to the content policy of the platform. This can be pre-approved as in the case of Netflix according to [content rating](https://en.wikipedia.org/wiki/Motion_picture_content_rating_system) of the media or can be strictly enforced like by YouTube.

This entire process is done by a machine learning model which performs copyright, piracy, and NSFW checks. If issues are found, we can push the task to a [dead-letter queue (DLQ)](https://karanpratapsingh.com/courses/system-design/message-queues#dead-letter-queues) and someone from the moderation team can do further inspection.

- **Transcoder**

[Transcoding](https://en.wikipedia.org/wiki/Transcoding) is a process in which the original data is decoded to an intermediate uncompressed format, which is then encoded into the target format. This process uses different [codecs](https://en.wikipedia.org/wiki/Video_codec) to perform bitrate adjustment, image downsampling, or re-encoding the media.

This results in a smaller size file and a much more optimized format for the target devices. Standalone solutions such as [FFmpeg](https://ffmpeg.org) or cloud-based solutions like [AWS Elemental MediaConvert](https://aws.amazon.com/mediaconvert) can be used to implement this step of the pipeline.

- **Quality Conversion**

This is the last step of the processing pipeline and as the name suggests, this step handles the conversion of the transcoded media from the previous step into different resolutions such as 4K, 1440p, 1080p, 720p, etc.

It allows us to fetch the desired quality of the video as per the user's request, and once the media file finishes processing, it gets uploaded to a distributed file storage such as [HDFS](https://karanpratapsingh.com/courses/system-design/storage#hdfs), [GlusterFS](https://www.gluster.org), or an [object storage](https://karanpratapsingh.com/courses/system-design/storage#object-storage) such as [Amazon S3](https://aws.amazon.com/s3) for later retrieval during streaming.

_Note: We can add additional steps such as subtitles and thumbnails generation as part of our pipeline._

**Why are we using a message queue?**

Processing videos as a long-running task and using a [message queue](https://karanpratapsingh.com/courses/system-design/message-queues) makes much more sense. It also decouples our video processing pipeline from the upload functionality. We can use something like [Amazon SQS](https://aws.amazon.com/sqs) or [RabbitMQ](https://www.rabbitmq.com) to support this.

### Video streaming

Video streaming is a challenging task from both the client and server perspectives. Moreover, internet connection speeds vary quite a lot between different users. To make sure users don't re-fetch the same content, we can use a [Content Delivery Network (CDN)](https://karanpratapsingh.com/courses/system-design/content-delivery-network).

Netflix takes this a step further with its [Open Connect](https://openconnect.netflix.com) program. In this approach, they partner with thousands of Internet Service Providers (ISPs) to localize their traffic and deliver their content more efficiently.

**What is the difference between Netflix's Open Connect and a traditional Content Delivery Network (CDN)?**

Netflix Open Connect is a purpose-built [Content Delivery Network (CDN)](https://karanpratapsingh.com/courses/system-design/content-delivery-network) responsible for serving Netflix's video traffic. Around 95% of the traffic globally is delivered via direct connections between Open Connect and the ISPs their customers use to access the internet.

Currently, they have Open Connect Appliances (OCAs) in over 1000 separate locations around the world. In case of issues, Open Connect Appliances (OCAs) can failover, and the traffic can be re-routed to Netflix servers.

Additionally, we can use [Adaptive bitrate streaming](https://en.wikipedia.org/wiki/Adaptive_bitrate_streaming) protocols such as [HTTP Live Streaming (HLS)](https://en.wikipedia.org/wiki/HTTP_Live_Streaming) which is designed for reliability and it dynamically adapts to network conditions by optimizing playback for the available speed of the connections.

Lastly, for playing the video from where the user left off (part of our extended requirements), we can simply use the `offset` property we stored in the `views` table to retrieve the scene chunk at that particular timestamp and resume the playback for the user.

### Searching

Sometimes traditional DBMS are not performant enough, we need something which allows us to store, search, and analyze huge volumes of data quickly and in near real-time and give results within milliseconds. [Elasticsearch](https://www.elastic.co) can help us with this use case.

[Elasticsearch](https://www.elastic.co) is a distributed, free and open search and analytics engine for all types of data, including textual, numerical, geospatial, structured, and unstructured. It is built on top of [Apache Lucene](https://lucene.apache.org).

**How do we identify trending content?**

Trending functionality will be based on top of the search functionality. We can cache the most frequently searched queries in the last `N` seconds and update them every `M` seconds using some sort of batch job mechanism.

### Sharing

Sharing content is an important part of any platform, for this, we can have some sort of URL shortener service in place that can generate short URLs for the users to share.

_For more details, refer to the [URL Shortener](https://karanpratapsingh.com/courses/system-design/url-shortener) system design._

## Detailed design

It's time to discuss our design decisions in detail.

### Data Partitioning

To scale out our databases we will need to partition our data. Horizontal partitioning (aka [Sharding](https://karanpratapsingh.com/courses/system-design/sharding)) can be a good first step. We can use partitions schemes such as:

- Hash-Based Partitioning
- List-Based Partitioning
- Range Based Partitioning
- Composite Partitioning

The above approaches can still cause uneven data and load distribution, we can solve this using [Consistent hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing).

_For more details, refer to [Sharding](https://karanpratapsingh.com/courses/system-design/sharding) and [Consistent Hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing)._

### Geo-blocking

Platforms like Netflix and YouTube use [Geo-blocking](https://en.wikipedia.org/wiki/Geo-blocking) to restrict content in certain geographical areas or countries. This is primarily done due to legal distribution laws that Netflix has to adhere to when they make a deal with the production and distribution companies. In the case of YouTube, this will be controlled by the user during the publishing of the content.

We can determine the user's location either using their [IP](https://karanpratapsingh.com/courses/system-design/ip) or region settings in their profile then use services like [Amazon CloudFront](https://aws.amazon.com/cloudfront) which supports a geographic restrictions feature or a [geolocation routing policy](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-geo.html) with [Amazon Route53](https://aws.amazon.com/route53) to restrict the content and re-route the user to an error page if the content is not available in that particular region or country.

### Recommendations

Netflix uses a machine learning model which uses the user's viewing history to predict what the user might like to watch next, an algorithm like [Collaborative Filtering](https://en.wikipedia.org/wiki/Collaborative_filtering) can be used.

However, Netflix (like YouTube) uses its own algorithm called Netflix Recommendation Engine which can track several data points such as:

- User profile information like age, gender, and location.
- Browsing and scrolling behavior of the user.
- Time and date a user watched a title.
- The device which was used to stream the content.
- The number of searches and what terms were searched.

_For more detail, refer to [Netflix recommendation research](https://research.netflix.com/research-area/recommendations)._

### Metrics and Analytics

Recording analytics and metrics is one of our extended requirements. We can capture the data from different services and run analytics on the data using [Apache Spark](https://spark.apache.org) which is an open-source unified analytics engine for large-scale data processing. Additionally, we can store critical metadata in the views table to increase data points within our data.

### Caching

In a streaming platform, caching is important. We have to be able to cache as much static media content as possible to improve user experience. We can use solutions like [Redis](https://redis.io) or [Memcached](https://memcached.org) but what kind of cache eviction policy would best fit our needs?

**Which cache eviction policy to use?**

[Least Recently Used (LRU)](<https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)>) can be a good policy for our system. In this policy, we discard the least recently used key first.

**How to handle cache miss?**

Whenever there is a cache miss, our servers can hit the database directly and update the cache with the new entries.

_For more details, refer to [Caching](https://karanpratapsingh.com/courses/system-design/caching)._

### Media streaming and storage

As most of our storage space will be used for storing media files such as thumbnails and videos. Per our discussion earlier, the media service will be handling both the upload and processing of media files.

We will use distributed file storage such as [HDFS](https://karanpratapsingh.com/courses/system-design/storage#hdfs), [GlusterFS](https://www.gluster.org), or an [object storage](https://karanpratapsingh.com/courses/system-design/storage#object-storage) such as [Amazon S3](https://aws.amazon.com/s3) for storage and streaming of the content.

### Content Delivery Network (CDN)

[Content Delivery Network (CDN)](https://karanpratapsingh.com/courses/system-design/content-delivery-network) increases content availability and redundancy while reducing bandwidth costs. Generally, static files such as images, and videos are served from CDN. We can use services like [Amazon CloudFront](https://aws.amazon.com/cloudfront) or [Cloudflare CDN](https://www.cloudflare.com/cdn) for this use case.

## Identify and resolve bottlenecks

![netflix-advanced-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/netflix/netflix-advanced-design.png)

Let us identify and resolve bottlenecks such as single points of failure in our design:

- "What if one of our services crashes?"
- "How will we distribute our traffic between our components?"
- "How can we reduce the load on our database?"
- "How to improve the availability of our cache?"

To make our system more resilient we can do the following:

- Running multiple instances of each of our services.
- Introducing [load balancers](https://karanpratapsingh.com/courses/system-design/load-balancing) between clients, servers, databases, and cache servers.
- Using multiple read replicas for our databases.
- Multiple instances and replicas for our distributed cache.


# Uber

Let's design an [Uber](https://uber.com) like ride-hailing service, similar to services like [Lyft](https://www.lyft.com), [OLA Cabs](https://www.olacabs.com), etc.

## What is Uber?

Uber is a mobility service provider, allowing users to book rides and a driver to transport them in a way similar to a taxi. It is available on the web and mobile platforms such as Android and iOS.

## Requirements

Our system should meet the following requirements:

### Functional requirements

We will design our system for two types of users: Customers and Drivers.

**Customers**

- Customers should be able to see all the cabs in the vicinity with an ETA and pricing information.
- Customers should be able to book a cab to a destination.
- Customers should be able to see the location of the driver.

**Drivers**

- Drivers should be able to accept or deny the customer-requested ride.
- Once a driver accepts the ride, they should see the pickup location of the customer.
- Drivers should be able to mark the trip as complete on reaching the destination.

### Non-Functional requirements

- High reliability.
- High availability with minimal latency.
- The system should be scalable and efficient.

### Extended requirements

- Customers can rate the trip after it's completed.
- Payment processing.
- Metrics and analytics.

## Estimation and Constraints

Let's start with the estimation and constraints.

_Note: Make sure to check any scale or traffic-related assumptions with your interviewer._

### Traffic

Let us assume we have 100 million daily active users (DAU) with 1 million drivers and on average our platform enables 10 million rides daily.

If on average each user performs 10 actions (such as request a check available rides, fares, book rides, etc.) we will have to handle 1 billion requests daily.

$$
100 \space million \times 10 \space actions = 1 \space billion/day
$$

**What would be Requests Per Second (RPS) for our system?**

1 billion requests per day translate into 12K requests per second.

$$
\frac{1 \space billion}{(24 \space hrs \times 3600 \space seconds)} = \sim 12K \space requests/second
$$

### Storage

If we assume each message on average is 400 bytes, we will require about 400 GB of database storage every day.

$$
1 \space billion \times 400 \space bytes = \sim 400 \space GB/day
$$

And for 10 years, we will require about 1.4 PB of storage.

$$
400 \space GB \times 10 \space years \times 365 \space days = \sim 1.4 \space PB
$$

### Bandwidth

As our system is handling 400 GB of ingress every day, we will require a minimum bandwidth of around 5 MB per second.

$$
\frac{400 \space GB}{(24 \space hrs \times 3600 \space seconds)} = \sim 5 \space MB/second
$$

### High-level estimate

Here is our high-level estimate:

| Type                      | Estimate    |
| ------------------------- | ----------- |
| Daily active users (DAU)  | 100 million |
| Requests per second (RPS) | 12K/s       |
| Storage (per day)         | ~400 GB     |
| Storage (10 years)        | ~1.4 PB     |
| Bandwidth                 | ~5 MB/s     |

## Data model design

This is the general data model which reflects our requirements.

![uber-datamodel](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/uber/uber-datamodel.png)

We have the following tables:

**customers**

This table will contain a customer's information such as `name`, `email`, and other details.

**drivers**

This table will contain a driver's information such as `name`, `email`, `dob` and other details.

**trips**

This table represents the trip taken by the customer and stores data such as `source`, `destination`, and `status` of the trip.

**cabs**

This table stores data such as the registration number, and type (like Uber Go, Uber XL, etc.) of the cab that the driver will be driving.

**ratings**

As the name suggests, this table stores the `rating` and `feedback` for the trip.

**payments**

The payments table contains the payment-related data with the corresponding `tripID`.

### What kind of database should we use?

While our data model seems quite relational, we don't necessarily need to store everything in a single database, as this can limit our scalability and quickly become a bottleneck.

We will split the data between different services each having ownership over a particular table. Then we can use a relational database such as [PostgreSQL](https://www.postgresql.org) or a distributed NoSQL database such as [Apache Cassandra](https://cassandra.apache.org/_/index.html) for our use case.

## API design

Let us do a basic API design for our services:

### Request a Ride

Through this API, customers will be able to request a ride.

```tsx
requestRide(customerID: UUID, source: Tuple<float>, destination: Tuple<float>, cabType: Enum<string>, paymentMethod: Enum<string>): Ride
```

**Parameters**

Customer ID (`UUID`): ID of the customer.

Source (`Tuple<float>`): Tuple containing the latitude and longitude of the trip's starting location.

Destination (`Tuple<float>`): Tuple containing the latitude and longitude of the trip's destination.

**Returns**

Result (`Ride`): Associated ride information of the trip.

### Cancel the Ride

This API will allow customers to cancel the ride.

```tsx
cancelRide(customerID: UUID, reason?: string): boolean
```

**Parameters**

Customer ID (`UUID`): ID of the customer.

Reason (`UUID`): Reason for canceling the ride _(optional)_.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Accept or Deny the Ride

This API will allow the driver to accept or deny the trip.

```tsx
acceptRide(driverID: UUID, rideID: UUID): boolean
denyRide(driverID: UUID, rideID: UUID): boolean
```

**Parameters**

Driver ID (`UUID`): ID of the driver.

Ride ID (`UUID`): ID of the customer requested ride.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Start or End the Trip

Using this API, a driver will be able to start and end the trip.

```tsx
startTrip(driverID: UUID, tripID: UUID): boolean
endTrip(driverID: UUID, tripID: UUID): boolean
```

**Parameters**

Driver ID (`UUID`): ID of the driver.

Trip ID (`UUID`): ID of the requested trip.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

### Rate the Trip

This API will enable customers to rate the trip.

```tsx
rateTrip(customerID: UUID, tripID: UUID, rating: int, feedback?: string): boolean
```

**Parameters**

Customer ID (`UUID`): ID of the customer.

Trip ID (`UUID`): ID of the completed trip.

Rating (`int`): Rating of the trip.

Feedback (`string`): Feedback about the trip by the customer _(optional)_.

**Returns**

Result (`boolean`): Represents whether the operation was successful or not.

## High-level design

Now let us do a high-level design of our system.

### Architecture

We will be using [microservices architecture](https://karanpratapsingh.com/courses/system-design/monoliths-microservices#microservices) since it will make it easier to horizontally scale and decouple our services. Each service will have ownership of its own data model. Let's try to divide our system into some core services.

**Customer Service**

This service handles customer-related concerns such as authentication and customer information.

**Driver Service**

This service handles driver-related concerns such as authentication and driver information.

**Ride Service**

This service will be responsible for ride matching and quadtree aggregation. It will be discussed in detail separately.

**Trip Service**

This service handles trip-related functionality in our system.

**Payment Service**

This service will be responsible for handling payments in our system.

**Notification Service**

This service will simply send push notifications to the users. It will be discussed in detail separately.

**Analytics Service**

This service will be used for metrics and analytics use cases.

**What about inter-service communication and service discovery?**

Since our architecture is microservices-based, services will be communicating with each other as well. Generally, REST or HTTP performs well but we can further improve the performance using [gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc#grpc) which is more lightweight and efficient.

[Service discovery](https://karanpratapsingh.com/courses/system-design/service-discovery) is another thing we will have to take into account. We can also use a service mesh that enables managed, observable, and secure communication between individual services.

_Note: Learn more about [REST, GraphQL, gRPC](https://karanpratapsingh.com/courses/system-design/rest-graphql-grpc) and how they compare with each other._

### How is the service expected to work?

Here's how our service is expected to work:

![uber-working](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/uber/uber-working.png)

1. Customer requests a ride by specifying the source, destination, cab type, payment method, etc.
2. Ride service registers this request, finds nearby drivers, and calculates the estimated time of arrival (ETA).
3. The request is then broadcasted to the nearby drivers for them to accept or deny.
4. If the driver accepts, the customer is notified about the live location of the driver with the estimated time of arrival (ETA) while they wait for pickup.
5. The customer is picked up and the driver can start the trip.
6. Once the destination is reached, the driver will mark the ride as complete and collect payment.
7. After the payment is complete, the customer can leave a rating and feedback for the trip if they like.

### Location Tracking

How do we efficiently send and receive live location data from the client (customers and drivers) to our backend? We have two different options:

**Pull model**

The client can periodically send an HTTP request to servers to report its current location and receive ETA and pricing information. This can be achieved via something like [Long polling](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#long-polling).

**Push model**

The client opens a long-lived connection with the server and once new data is available it will be pushed to the client. We can use [WebSockets](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#websockets) or [Server-Sent Events (SSE)](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#server-sent-events-sse) for this.

The pull model approach is not scalable as it will create unnecessary request overhead on our servers and most of the time the response will be empty, thus wasting our resources. To minimize latency, using the push model with [WebSockets](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#websockets) is a better choice because then we can push data to the client once it's available without any delay, given that the connection is open with the client. Also, WebSockets provide full-duplex communication, unlike [Server-Sent Events (SSE)](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events#server-sent-events-sse) which are only unidirectional.

Additionally, the client application should have some sort of background job mechanism to ping GPS location while the application is in the background.

_Note: Learn more about [Long polling, WebSockets, Server-Sent Events (SSE)](https://karanpratapsingh.com/courses/system-design/long-polling-websockets-server-sent-events)._

### Ride Matching

We need a way to efficiently store and query nearby drivers. Let's explore different solutions we can incorporate into our design.

**SQL**

We already have access to the latitude and longitude of our customers, and with databases like [PostgreSQL](https://www.postgresql.org) and [MySQL](https://www.mysql.com) we can perform a query to find nearby driver locations given a latitude and longitude (X, Y) within a radius (R).

```sql
SELECT * FROM locations WHERE lat BETWEEN X-R AND X+R AND long BETWEEN Y-R AND Y+R
```

However, this is not scalable, and performing this query on large datasets will be quite slow.

**Geohashing**

[Geohashing](https://karanpratapsingh.com/courses/system-design/geohashing-and-quadtrees#geohashing) is a [geocoding](https://en.wikipedia.org/wiki/Address_geocoding) method used to encode geographic coordinates such as latitude and longitude into short alphanumeric strings. It was created by [Gustavo Niemeyer](https://twitter.com/gniemeyer) in 2008.

Geohash is a hierarchical spatial index that uses Base-32 alphabet encoding, the first character in a geohash identifies the initial location as one of the 32 cells. This cell will also contain 32 cells. This means that to represent a point, the world is recursively divided into smaller and smaller cells with each additional bit until the desired precision is attained. The precision factor also determines the size of the cell.

![geohashing](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-IV/geohashing-and-quadtrees/geohashing.png)

For example, San Francisco with coordinates `37.7564, -122.4016` can be represented in geohash as `9q8yy9mf`.

Now, using the customer's geohash we can determine the nearest available driver by simply comparing it with the driver's geohash. For better performance, we will index and store the geohash of the driver in memory for faster retrieval.

**Quadtrees**

A [Quadtree](https://karanpratapsingh.com/courses/system-design/geohashing-and-quadtrees#quadtrees) is a tree data structure in which each internal node has exactly four children. They are often used to partition a two-dimensional space by recursively subdividing it into four quadrants or regions. Each child or leaf node stores spatial information. Quadtrees are the two-dimensional analog of [Octrees](https://en.wikipedia.org/wiki/Octree) which are used to partition three-dimensional space.

![quadtree](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-IV/geohashing-and-quadtrees/quadtree.png)

Quadtrees enable us to search points within a two-dimensional range efficiently, where those points are defined as latitude/longitude coordinates or as cartesian (x, y) coordinates.

We can save further computation by only subdividing a node after a certain threshold.

![quadtree-subdivision](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-IV/geohashing-and-quadtrees/quadtree-subdivision.png)

[Quadtree](https://karanpratapsingh.com/courses/system-design/geohashing-and-quadtrees#quadtrees) seems perfect for our use case, we can update the Quadtree every time we receive a new location update from the driver. To reduce the load on the quadtree servers we can use an in-memory datastore such as [Redis](https://redis.io) to cache the latest updates. And with the application of mapping algorithms such as the [Hilbert curve](https://en.wikipedia.org/wiki/Hilbert_curve), we can perform efficient range queries to find nearby drivers for the customer.

**What about race conditions?**

Race conditions can easily occur when a large number of customers will be requesting rides simultaneously. To avoid this, we can wrap our ride matching logic in a [Mutex](<https://en.wikipedia.org/wiki/Lock_(computer_science)>) to avoid any race conditions. Furthermore, every action should be transactional in nature.

_For more details, refer to [Transactions](https://karanpratapsingh.com/courses/system-design/transactions) and [Distributed Transactions](https://karanpratapsingh.com/courses/system-design/distributed-transactions)._

**How to find the best drivers nearby?**

Once we have a list of nearby drivers from the Quadtree servers, we can perform some sort of ranking based on parameters like average ratings, relevance, past customer feedback, etc. This will allow us to broadcast notifications to the best available drivers first.

**Dealing with high demand**

In cases of high demand, we can use the concept of Surge Pricing. Surge pricing is a dynamic pricing method where prices are temporarily increased as a reaction to increased demand and mostly limited supply. This surge price can be added to the base price of the trip.

_For more details, learn how [surge pricing works](https://www.uber.com/us/en/drive/driver-app/how-surge-works) with Uber._

### Payments

Handling payments at scale is challenging, to simplify our system we can use a third-party payment processor like [Stripe](https://stripe.com) or [PayPal](https://www.paypal.com). Once the payment is complete, the payment processor will redirect the user back to our application and we can set up a [webhook](https://en.wikipedia.org/wiki/Webhook) to capture all the payment-related data.

### Notifications

Push notifications will be an integral part of our platform. We can use a message queue or a message broker such as [Apache Kafka](https://kafka.apache.org) with the notification service to dispatch requests to [Firebase Cloud Messaging (FCM)](https://firebase.google.com/docs/cloud-messaging) or [Apple Push Notification Service (APNS)](https://developer.apple.com/documentation/usernotifications) which will handle the delivery of the push notifications to user devices.

_For more details, refer to the [WhatsApp](https://karanpratapsingh.com/courses/system-design/whatsapp#notifications) system design where we discuss push notifications in detail._

## Detailed design

It's time to discuss our design decisions in detail.

### Data Partitioning

To scale out our databases we will need to partition our data. Horizontal partitioning (aka [Sharding](https://karanpratapsingh.com/courses/system-design/sharding)) can be a good first step. We can shard our database either based on existing [partition schemes](https://karanpratapsingh.com/courses/system-design/sharding#partitioning-criteria) or regions. If we divide the locations into regions using let's say zip codes, we can effectively store all the data in a given region on a fixed node. But this can still cause uneven data and load distribution, we can solve this using [Consistent hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing).

_For more details, refer to [Sharding](https://karanpratapsingh.com/courses/system-design/sharding) and [Consistent Hashing](https://karanpratapsingh.com/courses/system-design/consistent-hashing)._

### Metrics and Analytics

Recording analytics and metrics is one of our extended requirements. We can capture the data from different services and run analytics on the data using [Apache Spark](https://spark.apache.org) which is an open-source unified analytics engine for large-scale data processing. Additionally, we can store critical metadata in the views table to increase data points within our data.

### Caching

In a location services-based platform, caching is important. We have to be able to cache the recent locations of the customers and drivers for fast retrieval. We can use solutions like [Redis](https://redis.io) or [Memcached](https://memcached.org) but what kind of cache eviction policy would best fit our needs?

**Which cache eviction policy to use?**

[Least Recently Used (LRU)](<https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_recently_used_(LRU)>) can be a good policy for our system. In this policy, we discard the least recently used key first.

**How to handle cache miss?**

Whenever there is a cache miss, our servers can hit the database directly and update the cache with the new entries.

_For more details, refer to [Caching](https://karanpratapsingh.com/courses/system-design/caching)._

## Identify and resolve bottlenecks

![uber-advanced-design](https://raw.githubusercontent.com/karanpratapsingh/portfolio/master/public/static/courses/system-design/chapter-V/uber/uber-advanced-design.png)

Let us identify and resolve bottlenecks such as single points of failure in our design:

- "What if one of our services crashes?"
- "How will we distribute our traffic between our components?"
- "How can we reduce the load on our database?"
- "How to improve the availability of our cache?"
- "How can we make our notification system more robust?"

To make our system more resilient we can do the following:

- Running multiple instances of each of our services.
- Introducing [load balancers](https://karanpratapsingh.com/courses/system-design/load-balancing) between clients, servers, databases, and cache servers.
- Using multiple read replicas for our databases.
- Multiple instances and replicas for our distributed cache.
- Exactly once delivery and message ordering is challenging in a distributed system, we can use a dedicated [message broker](https://karanpratapsingh.com/courses/system-design/message-brokers) such as [Apache Kafka](https://kafka.apache.org) or [NATS](https://nats.io) to make our notification system more robust.


