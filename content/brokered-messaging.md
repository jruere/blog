Title: A small survey of hosted brokered messaging systems
Date: 2015-11-15 21:45
Modified: 2016-02-28 19:23
Category: work
Tags: messaging, broker, net



# Azure Storage Queues

Intro: [1]

Pricing:
- https://azure.microsoft.com/en-us/pricing/details/storage/
- [2]

Protocols:
- HTTP, restful

Access control:
- Shared Key

Performance characteristics[1][4]:
- Max num of queues: inf
- Max msg size: 64KB
- Max num msgs: 500TB (for the entire storage account)
- Max persistence time: 7 days
(https://msdn.microsoft.com/en-us/library/azure/dd179346.aspx)
- Connections are not persistent[3]
- Batch receive: up to 32 msg
(https://msdn.microsoft.com/en-us/library/azure/dd179474.aspx)
- Batch send: 1 msg
(https://msdn.microsoft.com/en-us/library/azure/dd179346.aspx)
- Max throughput: target throughput for single queue (1 KB messages) up
to 2000 msgs/second[4]

Problems:
- Doesn't provide Topics: could be worked around with app code and
accepting some duplication on errors
- Opening a connection requires ~1s so this limits the throughput per
connection to ~32 recv/s and ~1 send/s


# Azure ServiceBus

Intro: https://azure.microsoft.com/en-us/documentation/services/service-bus/

Pricing:
- https://azure.microsoft.com/en-us/pricing/details/service-bus/
- [2]

Access control:
- Shared Key

Protocols:
- Custom (for .net)
- HTTP, restful
- AMQP 1.0 [5] (according to the docs, it should even work with
partitioned queues[6])

Performance characteristics[7]:
- Max num of queues: 10.000 (per service namespace)
- Max msg size: 256KB
- Max num msgs: 80GB (when using partitioning, otherwise 5GB)
- Max persistence time: unlimited
- Connections are not persistent on HTTP
- Connections are persistent on the other 2 protocols
- Batch receive:
-- HTTP: 1 msg
-- Others: yes
- Batch send:
-- HTTP: 1 msg
-- Others: yes
- Max concurrent clients: 100 TCP connections, no limit on HTTP clients
(bullshit!)
- Max throughput: target throughput for single queue (1 KB messages) up
to 2000 transactions/second (receiving is 2 operations, sending 1)

Problems:
- AMQP doesn't work with Python (I'll take another look this week). Update: [It was a build problem](https://issues.apache.org/jira/browse/PROTON-1087).
- HTTP connections start to fail after a given number.


# RackSpace Cloud Queues

Intro: [8]

Pricing:
- [8]
- http://www.rackspace.com/cloud/public-pricing/#bandwidth

Access control:
- ?

Protocols:
- HTTP, restful

Performance characteristics:
- Max num of queues:
- Max msg size: Less than 256KB
- Max num msgs:
- Max persistence time: 14 days
- Connections are not persistent
- Batch receive: 100 receive (depending on size), 25 delete
- Batch send: 25 (up to 256KB)
- Max concurrent clients:
- Max throughput:

Problems:
- Non persistent HTTP connections
- Performance?


# Amazon Simple Queue Service + Simple Notification Service

Topics are deconstructed into queues and a generic message multiplexing
service (like an exchange but for many services). Pretty nice.
Similar to Azure Storage Queues.

Intro:
-
http://gauravmantri.com/2012/03/27/comparing-windows-azure-queue-service-and-amazon-simple-queue-service/
- https://aws.amazon.com/sqs/
- https://docs.aws.amazon.com/sns/latest/dg/welcome.html

Pricing:
- https://aws.amazon.com/sqs/pricing/
- SNS is free for this purpose: https://aws.amazon.com/sns/pricing/

Access control:
- https://aws.amazon.com/iam/

Protocols:
- HTTP, restful

Performance characteristics[9]:
- Max num of queues:
- Max msg size: 64KB
- Max num msgs:
- Max persistence time: 4 days
- Connections are not persistent
- Batch receive: 10 msgs (probabilistic!)
- Batch send: up to 64KB or 10 msgs
- Max concurrent clients:
- Max throughput:

Problems:
- Non persistent HTTP connections
- Performance?


# CloudAMQP (Hosted RabbitMQ)

The service must be hosted on Heroku, AppHarbour, Bluemix or others.
Has a NewRelic plugin.
I'll focus on plan Big Bunny.

Intro:
- https://www.cloudamqp.com/
- http://blog.turret.io/rabbitmq-vs-amazon-sqs-a-short-comparison/
- https://www.cloudamqp.com/docs/faq.html#SLA

Pricing:
- 99USD/month (https://www.cloudamqp.com/plans.html)
- https://elements.heroku.com/addons/cloudamqp

Access control:
- LDAP or other SASL backends
- Plain over TLS

Protocols:
- AMQP 0.9.1
- AMQP 1.0?
- HTTPS
- Others

Performance characteristics:
- Max num of queues: inf
- Max msg size: big
- Max num msgs: inf
- Max persistence time: inf
- Batch receive:
- Batch send:
- Max concurrent clients: 1.000
- Max throughput: 10K msgs/s

Problems:
- Latency between data centers? Should be low. See:
https://www.cloudamqp.com/docs/faq.html#Available_data_centers
- Cannot easily change plan.


# PubNub

This one is a little weird. It has the additional feature of replaying
past messages. This is an awesome feature that we've implemented
ourselves and would be nice if we could delegate. It would mean 1 less
component (from the total 4 components) and also that we would depend on
PubNub.

Intro: https://www.pubnub.com/products/publish-subscribe/

Pricing:
- 4M msgs/day = 120M msgs/month = custom pricing
(https://www.pubnub.com/pricing/)

Access control:
- ?

Protocols:
- ?

Performance characteristics:
- Max num of queues:
- Max msg size:
- Max num msgs:
- Max persistence time:
- Batch receive:
- Batch send:
- Max concurrent clients:
- Max throughput:

Problems:
- No SLA until to top plan.
- Price!


# StormMQ

Looks awesome and dead.


Best Regards,
Javier


[1]
https://azure.microsoft.com/en-us/documentation/articles/storage-introduction/
[2] https://azure.microsoft.com/en-us/pricing/details/data-transfers/
[3] Each operation requires opening a new connection.
[4]
https://azure.microsoft.com/en-us/documentation/articles/azure-subscription-service-limits/#storage-limits
[5]
https://azure.microsoft.com/en-us/documentation/articles/service-bus-amqp-overview/
[6]
https://azure.microsoft.com/en-us/documentation/articles/service-bus-partitioned-queues-and-topics-amqp-overview/
[7]
https://azure.microsoft.com/en-us/documentation/articles/service-bus-azure-and-service-bus-queues-compared-contrasted/
[8] http://www.rackspace.com/cloud/queues
[9]
http://gauravmantri.com/2012/03/27/comparing-windows-azure-queue-service-and-amazon-simple-queue-service/


