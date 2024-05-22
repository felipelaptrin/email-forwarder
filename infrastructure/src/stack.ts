import { Duration, Stack, StackProps, Tags } from "aws-cdk-lib";
import { Construct } from "constructs";
import { DockerImageFunction, DockerImageCode } from "aws-cdk-lib/aws-lambda";
import path from "path";
import { StringParameter } from "aws-cdk-lib/aws-ssm";
import { InfraConfig } from "./config";
import { Rule, RuleTargetInput, Schedule } from "aws-cdk-lib/aws-events";
import { LambdaFunction } from "aws-cdk-lib/aws-events-targets";
import { Topic } from "aws-cdk-lib/aws-sns";
import { EmailSubscription } from "aws-cdk-lib/aws-sns-subscriptions";
import { RetentionDays } from "aws-cdk-lib/aws-logs";

export class EmailForwarderStack extends Stack {
  constructor(scope: Construct, id: string, config: InfraConfig, props?: StackProps) {
    super(scope, id, props);

    const topic = new Topic(this, "Topic", {
      topicName: "email-forwarder",
    });
    topic.addSubscription(new EmailSubscription(config.targetEmail));

    const lambda = new DockerImageFunction(this, "Lambda", {
      description:
        "Cron-based Lambda that checks new email of Gmail accounts and forward the title and sender of the email to another Gmail email",
      functionName: "email-forwarder",
      code: DockerImageCode.fromImageAsset(path.join(__dirname, "../../", "lambda")),
      environment: {
        SNS_TOPIC_ARN: topic.topicArn,
      },
      timeout: Duration.seconds(config.lambda.timeoutInSeconds),
      memorySize: config.lambda.memoryInMiB,
      deadLetterTopic: topic,
      architecture: config.lambda.architecture,
      logRetention: RetentionDays.ONE_WEEK
    });
    topic.grantPublish(lambda);

    for (const email of config.sourceEmail) {
      const [username, domain] = email.split("@");

      const parameterEmail = new StringParameter(this, `Email${username}`, {
        parameterName: `/email/${domain}/${username}/email`,
        stringValue: email,
      });
      parameterEmail.grantRead(lambda);
      const parameterPassword = new StringParameter(this, `Email${username}Password`, {
        parameterName: `/email/${domain}/${username}/password`,
        stringValue: "ChangeMe",
      });
      parameterPassword.grantRead(lambda);
      const parameterId = new StringParameter(this, `Email${username}LatestId`, {
        parameterName: `/email/${domain}/${username}/latest-id`,
        stringValue: "ThisWillBeManagedByTheLambda",
      });
      parameterId.grantRead(lambda);
      parameterId.grantWrite(lambda);

      const unit = config.lambda.triggerRateInMinutes == 1 ? "minute" : "minutes"
      const triggerRule = new Rule(this, `TriggerRule${username}`, {
        schedule: Schedule.expression(`rate(${config.lambda.triggerRateInMinutes} ${unit})`),
      });
      triggerRule.addTarget(
        new LambdaFunction(lambda, {
          event: RuleTargetInput.fromObject({
            parameterStore: {
              lastEmailIdRead: parameterId.parameterName,
              email: parameterEmail.parameterName,
              password: parameterPassword.parameterName,
            },
          }),
        }),
      );
    }

    Tags.of(this).add("Repository", "https://github.com/felipelaptrin/email-forwarder");
    Tags.of(this).add("ManagedBy", "CDK");
  }
}
