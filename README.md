### Инструкция по запуску

1. Добавление репозитория для установки postgres из helm 
```
helm repo add bitnami https://charts.bitnami.com/bitnami
```
2. Установка postgres
```
helm install postgres -f values-postgresql.yaml bitnami/postgresql
```
3. Запуск приложения
```
kubectl apply -f deployment.yaml
```
4. Запуск миграций
```
kubectl apply -f job.yaml
```