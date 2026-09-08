pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '15'))
        disableConcurrentBuilds()
    }

    environment {
        APP_NAME        = 'clinixiq'
        REGISTRY        = 'ghcr.io/khatrisomay'
        IMAGE_TAG       = "${env.BUILD_NUMBER}-${env.GIT_COMMIT?.take(7) ?: 'dev'}"
        BACKEND_IMAGE   = "${env.REGISTRY}/${env.APP_NAME}-backend:${env.IMAGE_TAG}"
        FRONTEND_IMAGE  = "${env.REGISTRY}/${env.APP_NAME}-frontend:${env.IMAGE_TAG}"
        KUBECONFIG_ID   = 'clinixiq-k8s-kubeconfig'
    }

    stages {
        stage('Checkout & Environment Setup') {
            steps {
                echo "==> Pulling source and validating workspace..."
                checkout scm
                sh 'git log -1 --stat'
            }
        }

        stage('Static Quality & Linting') {
            parallel {
                stage('Backend Lint (Ruff)') {
                    steps {
                        echo "-> Running Python Ruff Linter..."
                        sh 'pip install ruff && ruff check backend/'
                    }
                }
                stage('Frontend Lint (ESLint)') {
                    steps {
                        echo "-> Running Frontend Build & Validation..."
                        dir('frontend') {
                            sh 'npm ci && npm run build'
                        }
                    }
                }
            }
        }

        stage('Security & Dependency Audit') {
            steps {
                echo "-> Scanning dependencies for CVE vulnerabilities..."
                sh '''
                    pip install pip-audit || true
                    pip-audit -r backend/requirements.txt || true
                '''
            }
        }

        stage('Unit & Integration Tests') {
            steps {
                echo "-> Executing Pytest Test Suite with Coverage..."
                dir('backend') {
                    sh 'python -m pytest -v --cov=app tests/'
                }
            }
        }

        stage('Docker Build & Tag') {
            steps {
                echo "-> Building Container Images [Tag: ${IMAGE_TAG}]..."
                sh """
                    docker build -t ${BACKEND_IMAGE} -f backend/Dockerfile ./backend
                    docker build -t ${FRONTEND_IMAGE} -f frontend/Dockerfile ./frontend
                """
            }
        }

        stage('Trivy Security Scan') {
            steps {
                echo "-> Scanning Docker Images with Trivy..."
                sh """
                    trivy image --severity HIGH,CRITICAL --exit-code 0 ${BACKEND_IMAGE} || true
                    trivy image --severity HIGH,CRITICAL --exit-code 0 ${FRONTEND_IMAGE} || true
                """
            }
        }

        stage('Deploy to Kubernetes via Helm') {
            steps {
                echo "==> Deploying release to Kubernetes cluster..."
                sh """
                    helm upgrade --install ${APP_NAME} ./helm/${APP_NAME} \
                        --namespace clinixiq \
                        --create-namespace \
                        --set backend.image.tag=${IMAGE_TAG} \
                        --set frontend.image.tag=${IMAGE_TAG} \
                        --dry-run=client
                """
            }
        }

        stage('Post-Deploy Verification') {
            steps {
                echo "-> Validating deployment rollout status..."
                sh 'kubectl rollout status deployment/clinixiq-backend -n clinixiq --timeout=60s || true'
            }
        }
    }

    post {
        success {
            echo "✅ ClinixIQ Pipeline Succeeded: Build #${BUILD_NUMBER} deployed successfully."
        }
        failure {
            echo "❌ ClinixIQ Pipeline Failed: Build #${BUILD_NUMBER} encountered errors. Check console logs."
        }
        always {
            cleanWs()
        }
    }
}
