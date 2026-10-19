# Exercise 8 - Jenkins Hello World Job

`hello-world.sh` is the source-controlled build script for a Jenkins Freestyle job.

## Configure the job

1. In Jenkins, create a **Freestyle project** named `HelloWorld`.
2. Under **Source Code Management**, select Git and enter `https://github.com/akashmahesh2805/devops-submissions.git`. Add credentials only through Jenkins if the repository is private.
3. Under **Build Steps**, add **Execute shell**:

   ```sh
   sh "Exercise 8 - Jenkins Hello World Job/hello-world.sh"
   ```

4. Save the job, select **Build Now**, and confirm the Console Output contains `Hello, Jenkins!`.

Do not store a GitHub token or Jenkins password in this repository.
