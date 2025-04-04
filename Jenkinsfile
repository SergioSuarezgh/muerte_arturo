pipeline {
    agent any

    environment {
        BRANCH = 'main'
        REPO_URL = 'https://github.com/SergioSuarezgh/muerte_arturo.git'
    }

    stages {
        stage('Checkout del repositorio') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: "*/${env.BRANCH}"]],
                    userRemoteConfigs: [[
                        url: "${env.REPO_URL}",
                        credentialsId: 'github-token'
                    ]]
                ])
            }
        }

        stage('Leer versión actual') {
            steps {
                script {
                    def readme = readFile('README.md')
                    def matcher = readme =~ /[Vv]ers[ií]?[óo]?[n]?[:\s]*([0-9]+\.[0-9]+\.[0-9]+)/
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
                script {
                    // Actualizar README.md con la nueva versión
                    def readme = readFile('README.md')
                    def updated = readme.replaceFirst(env.OLD_VERSION, env.NEW_VERSION)
                    writeFile file: 'README.md', text: updated
        
                    // Obtener archivos modificados
                    sh '''
                        git diff --name-only HEAD~1 HEAD > cambios.txt || touch cambios.txt
                        echo "Versión: $NEW_VERSION" > version_log.txt
                        echo "Fecha: $(date)" >> version_log.txt
                        echo "Archivos modificados:" >> version_log.txt
                        cat cambios.txt >> version_log.txt
                    '''
                }
            }
        }

        stage('Commit y push de cambios') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'muerte_arturo', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                    sh '''
                        git config user.name "Jenkins CI"
                        git config user.email "jenkins@example.com"
                        git add README.md version_log.txt || true
                        git commit -m "🚀 Versión $NEW_VERSION generada automáticamente" || echo "Nada que commitear"
                        git push https://$GITHUB_USER:$GITHUB_TOKEN@github.com/SergioSuarezgh/muerte_arturo.git HEAD:main
                    '''
                }
            }
        }
    }
}
