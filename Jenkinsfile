pipeline {
    // This pipeline relies on there being only 1 agent that has the labels 'docker && amd64' and 1 
    // that has the labels 'docker && arm32v7'. If there are multiple then stashes must be implemented.
    agent none
    stages {
        stage('Build') {
            environment {
                DOCKER_REPO_SLUG = 'dullage/tahskr-server'
            }
            parallel {
                stage('Build (amd64)') {
                    agent { label 'docker && amd64' }
                    steps { sh 'docker build -t $DOCKER_REPO_SLUG:_amd64 $WORKSPACE' }
                }
                stage('Build (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps { sh 'docker build -t $DOCKER_REPO_SLUG:_arm32v7 $WORKSPACE' }
                }
            }
        }
        stage('Release') {
            when { branch 'master' }
            agent {
                dockerfile {
                    dir '.jenkins'
                    args '-v /etc/passwd:/etc/passwd:ro'
                }
            }
            environment {
                GIT_REPO_SLUG = 'Dullage/tahskr-server'
                GITHUB_TOKEN = credentials('github_token')
            }
            steps {
                sh 'bash $WORKSPACE/.jenkins/release.sh'
            }
        }
        stage('Deploy Builds') {
            when { branch 'master' }
            environment {
                DOCKER_REPO_SLUG = 'dullage/tahskr-server'
                DOCKER_CREDENTIALS = credentials('docker')
            }
            parallel {
                stage('Deploy (amd64)') {
                    agent { label 'docker && amd64' }
                    steps {
                        sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                        sh 'docker tag $DOCKER_REPO_SLUG:_amd64 $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-amd64'
                        sh 'docker push $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-amd64'
                    }
                }
                stage('Deploy (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps {
                        sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                        sh 'docker tag $DOCKER_REPO_SLUG:_arm32v7 $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-arm32v7'
                        sh 'docker push $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-arm32v7'
                    }
                }
            }
        }
        stage('Create & Deploy Manifest') {
            when { branch 'master' }
            agent { label 'docker' }
            environment {
                DOCKER_REPO_SLUG = 'dullage/tahskr-server'
                DOCKER_CREDENTIALS = credentials('docker')
                DOCKER_CLI_EXPERIMENTAL = 'enabled'
            }
            steps {
                sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                // Version
                sh 'docker manifest create $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION) $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-amd64 $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-arm32v7'
                sh 'docker manifest annotate $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION) $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-arm32v7 --variant v7'
                sh 'docker manifest push --purge $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)'
                // Latest
                sh 'docker manifest create $DOCKER_REPO_SLUG:latest $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-amd64 $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-arm32v7'
                sh 'docker manifest annotate $DOCKER_REPO_SLUG:latest $DOCKER_REPO_SLUG:$(cat $WORKSPACE/app/VERSION)-arm32v7 --variant v7'
                sh 'docker manifest push --purge $DOCKER_REPO_SLUG:latest'
            }
        }
        stage('Integrate') {
            when { anyOf { branch 'master'; branch 'develop' } }
            agent {
                dockerfile {
                    dir '.jenkins'
                    args '-v /etc/passwd:/etc/passwd:ro'
                }
            }
            environment {
                SSH_KEY = credentials('droplet_ssh_key')
                DEPLOY_IP = credentials('droplet_ip')
            }
            steps {
                sh 'bash $WORKSPACE/.jenkins/integrate.sh'
            }
        }
    }
}
