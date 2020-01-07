import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UserController } from './user/user.controller';
import { UserService } from './user/user.service';
import { TypeOrmModule } from '@nestjs/typeorm';
import {Connection} from "pg";
import { UserModule } from './user/user.module';
import { AuthModule } from './auth/auth.module';

@Module({
  imports: [
    TypeOrmModule.forRoot(),
    UserModule, AuthModule
  ],
  controllers: [
    AppController,
    UserController
  ],
  providers: [
    AppService,
    UserService
  ],
})
export class AppModule {
  constructor(private readonly connection: Connection) {

  }
}
