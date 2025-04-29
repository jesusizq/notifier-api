# Backend Challenge

## Description

The product department wants a system to be notified when a customer requests assistance from a bot. The bot will make an http call (like a webhook) with the following information:

- Topic: a string with values can be sales or pricing
- Description: a string with a description of the problem that needs assistance from.

You need to expose an API endpoint that will receive this call and depending on the selected topic will forward it to a different channel:

```
Topic    | Channel
----------------------
Sales    | Slack
Pricing  | Email
```

## Notes:

- Slack and Email are suggestions. Select one channel that you like the most, the other can be a mock.
- There may be more topics and channels in the future.

## The solution should:

- Be written in your favorite language and with the tools with which you feel comfortable.
- Be coded as you do daily (libraries, style, testing...).
- Be easy to grow with new functionality.
- Be a dockerized app.
