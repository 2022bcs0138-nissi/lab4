pipeline {
    agent any

    environment {
        IMAGE_NAME = "2022bcs0138nissiveronika/wine-mlops"
        BUILD_TAG = "${env.BUILD_NUMBER}"
        MODEL_IMPROVED = "false"
    }

    stages {

        // -------------------------
        // Stage 1: Checkout
        // -------------------------
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // -------------------------
        // Stage 2: Setup Python Virtual Environment
        // -------------------------
        stage('Setup Python Virtual Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        // -------------------------
        // Stage 3: Train Model
        // -------------------------
        stage('Train Model') {
            steps {
                sh '''
                . venv/bin/activate
                python scripts/train.py
                '''
            }
        }

        // -------------------------
        // Stage 4: Read Accuracy
        // -------------------------
        stage('Read Accuracy') {
            steps {
                script {
                    def metrics = readJSON file: 'app/artifacts/metrics.json'

                    env.CURRENT_R2 = metrics.r2.toString()
                    env.CURRENT_MSE = metrics.mse.toString()

                    echo "Current R2: ${env.CURRENT_R2}"
                    echo "Current MSE: ${env.CURRENT_MSE}"
                }
            }
        }

        // -------------------------
        // Stage 5: Compare Accuracy
        // -------------------------
        stage('Compare Accuracy') {
            steps {
                script {

                    withCredentials([string(credentialsId: 'best-metrics', variable: 'BEST_JSON')]) {

                        def best = readJSON text: BEST_JSON

                        float currentR2 = Float.parseFloat(env.CURRENT_R2)
                        float currentMSE = Float.parseFloat(env.CURRENT_MSE)

                        float bestR2 = Float.parseFloat(best.r2.toString())
                        float bestMSE = Float.parseFloat(best.mse.toString())

                        echo "Stored R2: ${bestR2}"
                        echo "Stored MSE: ${bestMSE}"

                        if (currentR2 > bestR2 && currentMSE < bestMSE) {

                            echo "Model improved on both R2 and MSE."
                            env.MODEL_IMPROVED = "true"

                        } else {

                            echo "Model did NOT improve."
                        }
                    }
                }
            }
        }

        // -------------------------
        // Stage 6: Build Docker Image (Conditional)
        // -------------------------
        stage('Build Docker Image') {
            when {
                expression { env.MODEL_IMPROVED == "true" }
            }
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        // -------------------------
        // Stage 7: Push Docker Image (Conditional)
        // -------------------------
        stage('Push Docker Image') {
            when {
                expression { env.MODEL_IMPROVED == "true" }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dock-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    sh '''
                    echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                    docker push ${IMAGE_NAME}:${BUILD_TAG}
                    docker push ${IMAGE_NAME}:latest
                    '''
                }
            }
        }
    }

    // -------------------------
    // Task 5: Archive Artifacts
    // -------------------------
    post {
        always {
            archiveArtifacts artifacts: 'app/artifacts/**', allowEmptyArchive: true
        }
    }
}
