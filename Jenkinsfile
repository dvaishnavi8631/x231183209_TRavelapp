pipeline {
    agent any
    environment {
        AWS_REGION = 'us-east-1'  // AWS region
        ECR_REGISTRY = '250738637992.dkr.ecr.us-east-1.amazonaws.com'  // Your ECR registry URL
        ECR_REPOSITORY = 'travel-sosh'  // ECR repository for your app
        SSO_PROFILE = 'MSCCLOUD-250738637992'  // AWS SSO profile name
        CLUSTER_NAME = 'x23183209-multicloud'  // EKS cluster name
        GIT_REPO = 'https://github.com/dvaishnavi8631/x231183209_TRavelapp.git'  // Your GitHub repository URL
    }
    stages {
        stage('Checkout Code') {
            steps {
                script {
                    echo 'Checking out the Git repository'
                    // Checkout the repository using GitHub credentials
                    checkout([$class: 'GitSCM', 
                        branches: [[name: '*/main']],  // Specify the branch to checkout
                        doGenerateSubmoduleConfigurations: false,
                        extensions: [],
                        userRemoteConfigs: [[
                            url: "${GIT_REPO}",
                            credentialsId: 'github-pat'  // Ensure this matches the Jenkins credentials ID for GitHub
                        ]])
                }
            }
        }
        stage('Login to AWS via SSO') {
            steps {
                script {
                    echo 'Ensure that AWS SSO login has been performed manually before this step.'
                    // Trigger SSO login using AWS CLI
                    sh "aws sso login --profile ${SSO_PROFILE} --region ${AWS_REGION}"
                }
            }
        }
        stage('Login to ECR') {
            steps {
                script {
                    echo 'Logging into AWS ECR'
                    // Get login password for ECR and login
                    def loginPassword = sh(script: "aws ecr get-login-password --region ${AWS_REGION} --profile ${SSO_PROFILE}", returnStdout: true).trim()
                    sh "docker login -u AWS -p ${loginPassword} ${ECR_REGISTRY}"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image'
                    // Build the Docker image with the tag from ECR repository
                    sh "docker build -t ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER} ."
                }
            }
        }
        stage('Push Docker Image to ECR') {
            steps {
                script {
                    echo 'Pushing Docker image to AWS ECR'
                    // Push the built image to ECR
                    sh "docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"
                }
            }
        }
        stage('Configure kubectl for EKS') {
            steps {
                script {
                    echo 'Configuring kubectl for EKS'
                    // Update kubeconfig for EKS to interact with the cluster
                    sh "aws eks --region ${AWS_REGION} update-kubeconfig --name ${CLUSTER_NAME} --profile ${SSO_PROFILE}"
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo 'Deploying to EKS'
                    // Update the deployment.yaml with the new image tag
                    sh "sed -i 's|<ECR-IMAGE-URL>|${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}|g' k8s/deployment.yaml"
                    // Apply the Kubernetes manifests to EKS
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
