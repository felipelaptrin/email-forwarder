import { Architecture } from "aws-cdk-lib/aws-lambda";

export interface LambdaProps {
  timeoutInSeconds: number;
  memoryInMiB: number;
  triggerRateInMinutes: number;
  architecture: Architecture;
}

export interface InfraConfig {
  sourceEmail: string[];
  targetEmail: string;
  lambda: LambdaProps;
}

export const config: InfraConfig = {
  sourceEmail: ["felipelaptrin@gmail.com", "paotrindadepao@gmail.com"],
  targetEmail: "emailsfelipetrindade@gmail.com",
  lambda: {
    timeoutInSeconds: 30,
    memoryInMiB: 256,
    triggerRateInMinutes: 1,
    architecture: Architecture.ARM_64, // This must match your architecture (since we are building during deployment)
  },
};
