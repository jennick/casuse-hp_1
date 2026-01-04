FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

COPY . .
RUN npm run build

#############################
# Runtime
#############################
FROM nginx:1.27-alpine

# verwijder default config
RUN rm /etc/nginx/conf.d/default.conf

# onze nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# build output
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
