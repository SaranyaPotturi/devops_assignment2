# use node lts
FROM node:18-alpine

# app dir
WORKDIR /app

# copy package manifest first for cache
COPY package.json package-lock.json* ./

RUN npm ci --only=production

# copy source
COPY . .

EXPOSE 3000
CMD ["node", "server.js"]
