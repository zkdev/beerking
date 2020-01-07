import {Entity, Column, PrimaryColumn, Unique, Index} from "typeorm";

@Entity()
export class User {

    @PrimaryColumn()
    uuid: string;

    @Column()
    @Index({unique: true})
    username: string;

    @Column()
    passwd: string;

    @Column()
    mail: string;

    @Column({ type: "timestamp", default: () => "CURRENT_TIMESTAMP"})
    time: string;

    @Column("simple-array")
    roles: string[];
}
