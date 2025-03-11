FROM public.ecr.aws/docker/library/node:22-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm ci 
COPY . .

RUN npm run build

FROM public.ecr.aws/nginx/nginx:1.27 as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]