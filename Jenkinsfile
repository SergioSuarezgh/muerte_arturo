pipeline {
    agent any

    environment {
        BRANCH = 'main'
        REPO_URL = 'https://github.com/<usuario>/<repositorio>.git'  // Reemplaza con tu repo
    }

    stages {
        stage('Checkout del repositorio') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH}"]],
                    userRemoteConfigs: [[
                        url: "${env.REPO_URL}",
                        credentialsId: 'github-token' // ID de la credencial guardada en Jenkins
                    ]]
                ])
            }
        }

        stage('Leer versión actual') {
            steps {
                script {
                    def readme = readFile('README.md')
                    def matcher = readme =~ /Versión:\s*(\d+\.\d+\.\d+)/
                    if (!matcher) {
                        error "No se encontró la versión en README.md"
                    }
                    env.OLD_VERSION = matcher[0][1]

                    def parts = env.OLD_VERSION.tokenize('.')
                    parts[-1] = (parts[-1].toInteger() + 1).toString()
                    env.NEW_VERSION = parts.join('.')
                }
            }
        }

        stage('Actualizar archivos') {
            steps {
                // Actualizar README.md con la nueva versión
                sh '''
                    sed -i "s/Versión: $OLD_VERSION/Versión: $NEW_VERSION/" README.md
                '''

                // Obtener los archivos modificados desde el último commit
                sh '''
                    git diff --name-only HEAD~1 HEAD > cambios.txt || touch cambios.txt
                '''

                // Crear archivo de log de versión
                sh '''
                    echo "Versión: $NEW_VERSION" > version_log.txt
                    echo "Fecha: $(date)" >> version_log.txt
                    echo "Archivos modificados:" >> version_log.txt
                    cat cambios.txt >> version_log.txt
                '''
            }
        }

        stage('Commit y push de cambios') {
            steps {
                sh '''
                    git config user.name "Jenkins CI"
                    git config user.email "jenkins@example.com"
                    git add README.md version_log.txt
                    git commit -m "🚀 Versión $NEW_VERSION generada automáticamente" || echo "Nada que commitear"
                    git push origin $BRANCH
                '''
            }
        }
    }
}
