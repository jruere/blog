Title: AMQP 1.0
Date: 2019-05-05 20:49
Category: play
Tags: networking, messaging, protocol, amqp

# Introduction

This is a WIP!

I have been using this protocol for years and it has been a bit of a pain, honestly.

In part because the library I use, [Qpid Proton](https://qpid.apache.org/proton/index.html), was a bit green and in part because I didn't fully understand the protocol when I begun.

Since the use of this protocol has expanded at work, it would be great to have a record of my experience with it to ease communication.

Finally, for reference, there's an [index of awesome links about AMQP](https://github.com/xinchen10/awesome-amqp).

# What is AMQP

AMQP 1.0 is a peer to peer reliable messaging protocol. It is quite sophisticated and allows for very good performance and several communication patterns.

The first most important thing to know about this protocol is that it is "AMQP 1.0". There are other versions (0.9 & 0-10) which are deeply different.
The worst part is that the other versions are more widely supported and most libraries and search results will be talking about these other /legacy/ versions.
For example, RabbitMQ supports 0.9 out of the box. On the other hand, Apache Qpid, ActiveMQ or Azure ServiceBus support 1.0.

# Resources

* [Super nice video intro](https://www.youtube.com/watch?v=ODpeIdUdClc&list=PLmE4bZU0qx-wAP02i0I7PJWvDWoCytEjD)
* [An article intro](https://dzone.com/refcardz/amqp-essentials?chapter=1)
* [Light overview](https://qpid.apache.org/releases/qpid-proton-0.27.1/proton/python/book/overview.html) from Qpid Proton.

# Features

## Peer to Peer

This feature is actually quite useful for testing as the broker and the rest of the system can be mocked quite easily.

## Delivery

The transmission of messages can have 3 levels of guarantee:

1. At-most-once: 1 or 0 times.
1. At-least-once: 1 or more times.
1. Exactly-once: 1 time.

At-most-once is the default for Qpid Proton and I suppose is useful for optional data or if the system is handling losing messages.

At-least-once, although theoretically impossible (the link may never be restored), works well in practice. It's important to handle duplicates or use idempotent messages.

Exactly-once is theoretically impossible and practically unlikely. I don't understand how this is seriously advertized.

The way these guarantees are implemented is by receivers accepting messages when they have been processed and senders settling messages once they are aware that the receiver accepted.

### Qpid Proton

Supports all guarantees and At-most-once is the default.

At-most-once is the default. In this mode, the receiver does not accept and the sender does not settle. It's fire and forget.

For At-least-once, the receiver accepts the message once it has been processed and the sender does not need to settle. If the accept did not reach the sender, it will send again eventually.

For exactly-once, the receiver does the same as At-least-once but will wait for the sender to *settle* the message. If the sender does not settle and the link breaks, it will be *accepted* again.
Hopefully the link will be restored and the receiver and sender will not have lost all state. 🤞

To get At-least-once with the Reactor API, use `auto_accept=False` in the constructor of the `MessagingHandler` and leave the rest as default.

## Flow Control

As a receiver, it is possible to specify how many messages you'd like to receive without any sort of synchronization. This is fantastic as it allows to minimize the problem of latency, there will be messages ready on the wire for the system.

# Other Interesting Features to Explore

## Bidirectional Communication

The protocol supports maintaining a relation between a message sent and one received. This allows to implement request-response easily.

It could be interesting to consider this protocol for this access pattern for 2 reasons:

1. It's pretty space efficient.
1. It allows for efficient async request-response.
1. It can allow to use a broker as a buffer or load-balancer.

## A Better HTTP?

Using nodes within a container arranged in a hierarchy allows to handle different stages of communication in different components.

This sounds like something I like doing in RESTfull APIs where there could be something like: /user/123/tweet/54/comment/9/
