locals {
  group_policies = {
    Dev-Team = {
      policy_name = "DevTeamPolicy"
      file_name   = "dev-team-policy.json"
    }
    Ops-Team = {
      policy_name = "OpsTeamPolicy"
      file_name   = "ops-team-policy.json"
    }
    SecOps-Team = {
      policy_name = "SecOpsTeamPolicy"
      file_name   = "secops-team-policy.json"
    }
  }

  user_groups = {
    roberto = ["Dev-Team"]
    sandra  = ["Dev-Team"]
    alicia  = ["Dev-Team", "SecOps-Team"]
    marta   = ["Ops-Team"]
    alexis  = ["Ops-Team"]
    camila  = ["SecOps-Team"]
  }
}
