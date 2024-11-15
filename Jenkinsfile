pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'  // AWS region
        ECR_REGISTRY = '250738637992.dkr.ecr.us-east-1.amazonaws.com'  // Your ECR registry URL
        ECR_REPOSITORY = 'travel-sosh'  // ECR repository for your app
        SSO_PROFILE = 'MSCCLOUD-250738637992'  // AWS SSO profile name
        CLUSTER_NAME = 'your-eks-cluster'  // EKS cluster name
    }
    stages {
        stage('Login to AWS via SSO') {
            steps {
                script {
                    echo 'Ensure that AWS SSO login has been performed manually before this step.'
                    // Trigger SSO login automatically (if supported by the environment)
                    sh "aws sso login --profile ${SSO_PROFILE} --region ${AWS_REGION}"
                }
            }
        }
        stage('Login to ECR') {
            steps {
                script {
                    // Log into ECR using AWS CLI
                    def loginPassword = sh(script: "aws ecr get-login-password --region ${AWS_REGION} --profile ${SSO_PROFILE}", returnStdout: true).trim()
                    sh "docker login -u AWS -p ${loginPassword} ${ECR_REGISTRY}"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image for your Django app
                    sh "docker build -t ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER} ."
                }
            }
        }
        stage('Push Docker Image to ECR') {
            steps {
                script {
                    // Push the Docker image to ECR
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"
                }
            }
        }
        stage('Configure kubectl for EKS') {
            steps {
                script {
                    // Configure kubectl to use the EKS cluster
                    sh "aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME} --profile ${SSO_PROFILE}"
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    // Update deployment.yaml with the new image tag
                    sh """
                        sed -i 's|<ECR-IMAGE-URL>|${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}|g' k8s/deployment.yaml
                    """
                    // Apply Kubernetes manifests
                    sh "kubectl apply -f k8s/"
                }
            }
        }
    }
    post {
        success {
            echo "Deployment to EKS successful!"
        }
        failure {
            echo "Deployment to EKS failed."
        }
    }
}
