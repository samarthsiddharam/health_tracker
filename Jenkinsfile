pipeline {
    agent any   // run on any available Jenkins node

    environment {
        VENV = "venv"
        // You can add DJANGO_SETTINGS_MODULE if needed
        // DJANGO_SETTINGS_MODULE = "myproject.settings"
    }

    stages {
        stage('Checkout') {
            steps {
                // Jenkins automatically checks out when using "pipeline from SCM",
                // but this is explicit and safe:
                checkout scm
            }
        }

        stage('Set up Python & install dependencies') {
            steps {
                sh """
                    python3 -m venv ${VENV}
                    . ${VENV}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run tests') {
            steps {
                sh """
                    . ${VENV}/bin/activate
                    python manage.py test
                """
            }
        }

        stage('Migrate database') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    . ${VENV}/bin/activate
                    python manage.py migrate --noinput
                """
            }
        }

        stage('Collect static files') {
            when {
                branch 'main'
            }
            steps {
                sh """
                    . ${VENV}/bin/activate
                    python manage.py collectstatic --noinput
                """
            }
        }

        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                // This part depends on how your college wants you to deploy.
                // For now, we just log a message.
                sh """
                    echo "Deployment step goes here (e.g., restart gunicorn/service)"
                """
            }
        }
    }

    post {
        always {
            echo "Build finished. Check above logs for details."
        }
        success {
            echo "Pipeline succeeded!"
        }
        failure {
            echo "Pipeline failed. Please check the error logs."
        }
    }
}
