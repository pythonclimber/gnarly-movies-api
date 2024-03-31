export interface Movie {
    _id: string;
    title: string;
    description: string;
    userId: string;
    director: string;
    imdbid: string;
    favorite: boolean;
    year?: string;
    runtime?: string;
    genres?: string;
    writer?: string;
    actors?: string;
    plot?: string;
    poster?: string;
    wishlist: boolean;
    format: string;
    rating?: number;
}

export interface User {
    username: string;
    password: string;
    emailAddress: string;
    firstName: string;
    lastName: string;
}