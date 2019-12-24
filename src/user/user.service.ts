import { Injectable } from '@nestjs/common';
import { RegisterUserDto } from '../register-user-dto';
import {User} from "../entity/User";
import "reflect-metadata";

@Injectable()
export class UserService {
  public register(data: RegisterUserDto): User {
    const uuidv4 = require('uuid/v4');
    const user = new User(uuidv4(), data);

    //TODO add user to database


    return user;
  }
}
