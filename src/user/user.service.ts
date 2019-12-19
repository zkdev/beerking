import { Injectable } from '@nestjs/common';
import { RegisterUserDto } from '../register-user-dto';
import { User } from '../user';

@Injectable()
export class UserService {
  public register(data: RegisterUserDto): User {
    const uuidv4 = require('uuid/v4');
    return new User(uuidv4(), data);
  }
}
