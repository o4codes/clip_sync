import _ from 'lodash';


export function parseObjectToCamelCase(obj: { [key: string]: string }): { [key: string]: string } {
    return Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [_.camelCase(key), value])
    );
}

export function parseObjectToSnakeCase(obj: { [key: string]: string }): { [key: string]: string } {
    return Object.fromEntries(
        Object.entries(obj).map(([key, value]) => [_.snakeCase(key), value])
    );
}