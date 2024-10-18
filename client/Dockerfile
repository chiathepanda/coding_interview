# build vite project as builder
FROM node:20.18.0-alpine 
# AS builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

RUN npm run build

COPY . .

FROM node:20.18.0-alpine

# WORKDIR /app

# COPY --from=builder /app/dist ./dist
# COPY --from=builder /app/server.js ./server.js
# COPY --from=builder /app/package.json ./package.json
# COPY --from=builder /app/package-lock.json ./package-lock.json

# # exclude devDependencies for smaller size
# RUN npm install --only=production

EXPOSE 3000

# Use express framework of Node.js
CMD ["npm", "start"]
