import { IsEmail, Length } from 'class-validator';

export class RegisterUserDto {
  @IsEmail()
  mail: string;
  @Length(3, 15)
  username: string;
  @Length(127) // SHA512
  passwd: string;
}
