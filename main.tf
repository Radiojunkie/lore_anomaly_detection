provider "aws" {
  region = "us-east-1"
}

resource "aws_ecs_cluster" "anomaly_detection_cluster" {
  name = "anomaly-detection-cluster"
}

resource "aws_ecs_task_definition" "anomaly_detection_task" {
  family       = "anomaly-detection"
  container_definitions = jsonencode([
    {
      name      = "anomaly-detection",
      image     = "<aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/anomaly-detection",
      memory    = 512,
      cpu       = 256,
      essential = true
    }
  ])
}

resource "aws_ecs_service" "anomaly_service" {
  name            = "anomaly-service"
  cluster         = aws_ecs_cluster.anomaly_detection_cluster.id
  task_definition = aws_ecs_task_definition.anomaly_detection_task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
}
