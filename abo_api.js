@Override
public APIStatus handleUnverifiedRequest(String requestString, JSONObject request, JSONObject response, String ip, String purpose) {
  return handleLeaderboardRequest(requestString, request, response, null, ip, purpose);
}

/**
  * Because unverified requests seem to hang for now, allow both verified and unverified access to the leaderboard
  */
private APIStatus handleLeaderboardRequest(String requestString, JSONObject request, JSONObject response, User user, String ip, String purpose) {
  // Needs to opt not get since this is called internally as well (without this param)
  int pos = request.optInt("position", 0);
  int count = Math.min(LeaderboardManager.MAX_ELEMENTS, request.optInt("count", 15));
  
  switch (purpose) {
  case "get": {
    Type leaderboardType = Type.valueOf(request.optString("leaderboardType", Type.ArenaRating.name()));
    boolean showUserPageDirectly = false;
    Collection<LeaderboardUser> userList = null;
    LeaderboardUser userToShow = null;
    if (pos == -1) {
      if (request.has("name")) {
        userList = leaderboardManager.getUsersPage(request.getString("name"), count, leaderboardType);
        if (userList == null) {
          userToShow = leaderboardManager.getInactiveUserPage(request.getString("name"));
          if (userToShow == null) {
            return APIStatus.err(StatusCode.NOT_FOUND);
          } else {
            showUserPageDirectly = true;
          }			
        }
      }
      else {
        // In theory, this condition should never result in an inactive user
        // assuming this condition can only be called by the user retrieving their own position
        ObjectId userId = new ObjectId(request.getString("userId"));
        userList = leaderboardManager.getOwnUsersPage(userId, count, leaderboardType);
        if (userList == null) {
          return APIStatus.err(StatusCode.NOT_FOUND);
        }
      }
    }
    else {
      userList = leaderboardManager.getUsersPage(pos, count, leaderboardType);
    }
    if (showUserPageDirectly) {
      response.put("userToShow", userToShow.createJson(leaderboardType));
    } else {
      JSONArray jsonUsers = new JSONArray();
      for (LeaderboardUser lUser : userList) {
        JSONObject jsonUser = lUser.createJson(leaderboardType);
        jsonUsers.put(jsonUser);
      }
      response.put("users", jsonUsers);
    }
    List<Integer> activeLeaderboardTypes = new ArrayList<Integer>();
    for(ActiveType type : LeaderboardUserCollections.ActiveType.values()) {
      activeLeaderboardTypes.add(type.getValue());
    }
    
    response.put("showUserPageDirectly", showUserPageDirectly);
    response.put("activeLeaderboardTypes", activeLeaderboardTypes);
    break;
  }
  case "getLeaderboardUser": {
    ObjectId userId = new ObjectId(request.getString("userId"));
    LeaderboardUser lUser = leaderboardManager.getUser(userId);
    if(lUser != null) {
      response.put("lUser", lUser.createJson());
    }
    else {
      return APIStatus.err(StatusCode.NOT_FOUND);
    }
    break;
  }
  case "getHallOfFame": {
    Collection<LeaderboardUser> userList;
    int season = request.getInt("season");
    String leaderboardType = request.getString("leaderboardType");
    userList = leaderboardManager.getHallOfFamePage(season, leaderboardType, pos, count);
    
    JSONArray jsonUsers = new JSONArray();
    for (LeaderboardUser lUser : userList) {
      JSONObject jsonUser = lUser.createJson(Type.valueOf(leaderboardType));
      jsonUsers.put(jsonUser);
    }
    response.put("users", jsonUsers);
    break;
  }
  case "getGuildHallOfFame": {
    Collection<LeaderboardGuild> guildList;
    int season = request.getInt("season");
    guildList = leaderboardManager.getGuildHallOfFamePage(season, pos, count);
    
    JSONArray jsonGuilds = new JSONArray();
    for (LeaderboardGuild guild : guildList) {
      JSONObject jsonGuild = guild.createJson();
      jsonGuilds.put(jsonGuild);
    }
    response.put("guilds", jsonGuilds);
    break;
  }
  case "getGuilds": {
    Collection<LeaderboardGuild> guildList;
    if (pos == -1) {
      if (request.has("name")) {
        guildList = leaderboardManager.getGuildsPage(request.getString("name"), count);
        if (guildList == null) {
          return APIStatus.err(StatusCode.NOT_FOUND);
        }
      } else {
        ObjectId guildId = new ObjectId(request.getString("guildId"));
        guildList = leaderboardManager.getGuildsPage(guildId, count);
      }
    } else {
      guildList = leaderboardManager.getGuildsPage(pos, count);
    }
    JSONArray jsonGuilds = new JSONArray();
    for (LeaderboardGuild guild : guildList) {
      JSONObject jsonGuild = guild.createJson();
      jsonGuilds.put(jsonGuild);
    }
    response.put("guilds", jsonGuilds);
    if(user != null) {
      response.put("currentSeasonInstance", userGuildRewardPoolManager.getUserCurrentGuildRewardPool(user.getId()).createJson());
    }
    response.put("seasonRewardDistributionList", GenericFunctions.toJson(rankManager.getDistributionList()));
    break;
  }
  case "getBrowseGuilds": {
    int rating = request.getInt("rating");
    if (pos == -1) {
      pos = 0;
    }
    Collection<LeaderboardGuild> guildList = leaderboardManager.getBrowseGuildsPage(rating, pos, count);
    leaderboardManager.setBrowseGuildHasApplied((List<LeaderboardGuild>) guildList, new ObjectId(request.getString("userId")));
    JSONArray jsonGuilds = new JSONArray();
    for (LeaderboardGuild guild : guildList) {
      JSONObject jsonGuild = guild.createJson();
      jsonGuilds.put(jsonGuild);
    }
    response.put("browseGuilds", jsonGuilds);
    break;
  }
  case "getSpecificGuilds": {
    JSONArray guildIds = request.getJSONArray("guildIds");
    if (null == guildIds) {
      return APIStatus.err(StatusCode.BAD_REQUEST);
    }

    JSONArray jsonGuilds = new JSONArray();
    for (int i = 0; i < guildIds.length(); ++i) {
      ObjectId guildObjectId = new ObjectId(guildIds.getString(i));
      LeaderboardGuild guild = leaderboardManager.getGuild(guildObjectId);
      if (null != guild) {
        jsonGuilds.put(guild.createJson());
      }
      else {
        return APIStatus.err(StatusCode.NOT_FOUND);
      }
    }
    response.put("guilds", jsonGuilds);
    break;
  }
  default:
    loggingManager.logError("Purpose is invalid", StatusCode.BAD_REQUEST, requestString,
        response.toString(), null, ip, getPath(), purpose);
    return APIStatus.err(StatusCode.BAD_REQUEST);
  }
  return APIStatus.ok();
}