#!/usr/bin/env ts-node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { EmailForwarderStack } from "./stack";
import { config } from "./config";

const app = new cdk.App();

new EmailForwarderStack(app, "Stack", config);
