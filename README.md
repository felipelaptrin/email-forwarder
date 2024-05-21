# email-forwarder

The entire documentation about this project is presented in my [blog post](https://felipetrindade.com/email-forwarder).


## Pricing

AWS offers a generous free tier for the services we use:

- `Parameter Store`: Standard parameters are free. The interaction (retrieve/update value) with the parameter costs `$0.05` per 10,000 interactions.
- `EventBridge Rule`: Free for our use case.
- `SNS`: 1,000 notifications are free, after that $2 per 100,000 notifications.
- `Lambda`: This varies based on the memory and execution time of the Lambda. Using a Lambda of 512MB and 5s for each execution and running every 1 minute we will use around `110,000GB-s/month`. The free tier is 1 million invocations per month and 400,000Gb-s of compute time. So for us, this will be free.

So this is very likely to be free for you!

## Deployment

To make it more user-friendly I will do a step-by-step guide to help you setup all of this. Follow this in order!

### Gmail settings

The first thing we need to do is to access your [Gmail settings](https://mail.google.com/mail/u/0/#settings/general) and make sure the `IMAP` is enabled (check the `Forwarding and POP/IMAP` tab).

After that let's create a new App Password for us to use with the IMAP.

1) Access [Google Settings](https://myaccount.google.com/?hl=en)

![Google Settings](https://github.com/felipelaptrin/felipetrindade.com/blob/main/frontend/content/blog/email-forwarder/assets/gmail/google-settings.png)

2) Search for `App Passwords`

![Google Setting App Passwords](https://github.com/felipelaptrin/felipetrindade.com/blob/main/frontend/content/blog/email-forwarder/assets/gmail/google-app-passwords.png)

3) Create a new app password and copy the password value after creation

![Creating a new App Password](https://github.com/felipelaptrin/felipetrindade.com/blob/main/frontend/content/blog/email-forwarder/assets/gmail/google-app-passwords-creation.png)

Make sure to do all these steps in the email accounts you want to secure, in my case I have two (so I did this for both accounts).

### Infrastructure deployment

To make the development live easier I set up [DevBox](https://www.jetify.com/devbox/docs/) in the project. So you only need to have DevBox installed and run `devbox shell` to install all the dependencies of the project (NodeJS, Yarn...).

1) Install the dependencies

```sh
devbox shell
```

2) Move to the `infrastructure` folder

```sh
cd infrastructure
```

3) Install NodeJS dependencies

```sh
yarn
```

4) Modify the `config.ts` file accordingly

5) Deploy the infrastructure

```sh
yarn cdk deploy
```

Make you have AWS credentials setup in place and that your account-region is already [CDK bootstraped](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html).

6) Check the receiver email and accept the subscribe email from Amazon SNS

![Email inbox - accepting AWS SNS topic](https://github.com/felipelaptrin/felipetrindade.com/blob/main/frontend/content/blog/email-forwarder/assets/gmail/inbox.png)

6) Go to the AWS console and update the parameter(s) that contain your password (e.g. `/email/gmail.com/<YOUR_EMAIL>/password`) to used the app password you copied.

## Final result

Finally! Now we are receiving our forwarded emails as expected!

![Screenshot inbox from receiver email](https://github.com/felipelaptrin/felipetrindade.com/blob/main/frontend/content/blog/email-forwarder/assets/gmail/inbox-receiver.png)


![Screenshot email from receiver email](https://github.com/felipelaptrin/felipetrindade.com/blob/main/frontend/content/blog/email-forwarder/assets/gmail/email.png)
