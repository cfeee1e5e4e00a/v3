export enum Role {
    ADMIN,
}

export type User = {
    username: string;
    roles: Array<Role>;
};
