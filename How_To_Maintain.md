How to Maintain
---

There are three accounts that you will need to run a copy of this project, [GitLab](https://gitlab.com/users/sign_up), [Heroku](https://signup.heroku.com/login), [Discord Developer](https://discord.com/developers/docs/intro).


## GitLab
Once you have your GitLab account you will need to clone this project.
The only configuration needed is for environment variables but that can't be set up until the heroku step is completed.


## Heroku
Heroku is the platform that the bot runs on. If you add a credit card you get over 1000 hours a month which is more than enough.
It is also easy to deploy to and a clone of this repo will automatically. Once you have an account and app created add your deploy token and app names as environment variables.


## Discord Developer
Discord Developer is a key part to this project. Once the repo has been cloned you will need to create an bot and use the credentials that are given. There a lot of enviroment variables that need to be filled out. 

role variables should be in the <@role_id> format.
Current list:
1. CHANNEL_ID
2. GUILD_ID
3. LOG_LEVEL
4. leader_role
5. mod_role
6. student_role
7. alumni_role
8. professor_role
9. OWNER_ID
10. OWNER_NAME
11. REDIS_URL (Should be filled out automatically on Heroku)
12. homework_channel
13. troubleshooting_channel