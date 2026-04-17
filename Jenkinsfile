pipeline {
    agent any

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['PreProd', 'Production'],
            description: 'Target environment'
        )
        string(
            name: 'S3_BUCKET',
            defaultValue: 'my-lambda-usecase',
            description: 'S3 bucket to upload Lambda zip'
        )
        string(
            name: 'LAMBDA_NAME',
            defaultValue: 'ec2-event-slack-notifier',
            description: 'Lambda function name'
        )
        choice(
            name: 'AWS_REGION',
            choices: ['us-east-1', 'eu-west-1', 'ap-southeast-1'],
            description: 'AWS region'
        )
    }

    environment {
        ZIP_NAME = "${params.LAMBDA_NAME}.zip"
        PACKAGE_DIR = "package"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Prepare Package') {
            steps {
                sh '''
                  set -e
                  echo "Cleaning old package..."
                  rm -rf ${PACKAGE_DIR} ${ZIP_NAME}
                  mkdir -p ${PACKAGE_DIR}

                  echo "Installing dependencies..."
                  pip3 install -r slackmessenger_requirements.txt -t ${PACKAGE_DIR}

                  echo "Copying lambda source..."
                  cp slackmessenger.py ${PACKAGE_DIR}
                '''
            }
        }

        stage('Create Zip') {
            steps {
                sh '''
                  cd ${PACKAGE_DIR}
                  zip -r ../${ZIP_NAME} .
                '''
            }
        }

        stage('Upload to S3') {
            steps {
                withCredentials([
                    [$class: 'AmazonWebServicesCredentialsBinding',
                     credentialsId: 'aws-credentials']
                ]) {
                    sh '''
                      aws s3 mb s3://${LAMBDA_NAME} --region ${AWS_REGION}
                      echo "${LAMBDA_NAME} created successfully"
                      echo "Uploading ${ZIP_NAME} to ${LAMBDA_NAME} bucket" 
                      aws s3 cp ${ZIP_NAME} \
                        s3://${S3_BUCKET}/${ENVIRONMENT}/${LAMBDA_NAME}/${ZIP_NAME} \
                        --region ${AWS_REGION}
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Lambda package uploaded to S3 successfully"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
