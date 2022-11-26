# Development environment setup script
#
# Usage: source setup.sh
# Unfortunatelly, this script is not supported on Windows.

echo "Setting environment variables for development:"
export DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/db"
export IPFS_URL="http://127.0.0.1:9094"
export SECRET="1234"
echo " - DATABASE_URL: '$DATABASE_URL'"
echo " - IPFS_URL: '$IPFS_URL'"
echo " - SECRET: '$SECRET'"

if [ ! -f /tmp/containers-init ]; then
	echo "Starting containers..."
	export DOCKER_FOUND=0
	export DOCKER_CHECK="ps"

	echo "Checking for container backend..."

	if [ $DOCKER_FOUND != 1 ]; then
		echo "Trying docker..."
		export DOCKER_BIN="docker"
		$DOCKER_BIN $DOCKER_CHECK &> /dev/null
		if [ $? = 0 ]; then
			export DOCKER_FOUND=1
		fi
	fi

	if [ $DOCKER_FOUND != 1 ]; then
		echo "Docker not found, trying podman..."
		export DOCKER_BIN="podman"
		$DOCKER_BIN $DOCKER_CHECK &> /dev/null
		if [ $? = 0 ]; then
			export DOCKER_FOUND=1
		fi
	fi

	if [ $DOCKER_FOUND = 1 ]; then
		echo "Using '$DOCKER_BIN' container backend"

		echo "Launching db..."
		$DOCKER_BIN rm -f db &> /dev/null || true
		$DOCKER_BIN run -d --rm \
			--name db -p 5432:5432 \
			-e POSTGRES_PASSWORD="password" \
			-e POSTGRES_USER="user" \
			-e POSTGRES_DB="db" \
			docker.io/postgres:alpine

		echo "Launching ipfs..."
		$DOCKER_BIN rm -f ipfs &> /dev/null || true
		$DOCKER_BIN run -d --rm \
			--name ipfs -p 5001:5001 \
			docker.io/ipfs/kubo

		echo "Launching ipfs-cluster..."
		$DOCKER_BIN rm -f ipfs-cluster &> /dev/null || true
		$DOCKER_BIN run -d --rm \
			--name ipfs-cluster --net host \
			-e CLUSTER_RESTAPI_HTTPLISTENMULTIADDRESS="/ip4/0.0.0.0/tcp/9094" \
			docker.io/ipfs/ipfs-cluster

		echo "Waiting 5 seconds for containers to start..."
		sleep 5

		echo "Applying migrations..."
		python -m intape db migrate
	else
		echo "Container engine not found, skipping environment initialization"
	fi

	touch /tmp/containers-init
else
	echo "Containers already started, skipping..."
	echo " - (delete '/tmp/containers-init' to force restart them)"
fi

echo "Activating virtualenv..."
poetry shell
