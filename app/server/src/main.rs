#[get("/aws")]
fn hello1() -> &'static str {
    "Success"
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/api", routes![hello])
}