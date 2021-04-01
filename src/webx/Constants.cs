using System;

internal static class Constants
{
    // public static string UsersUrl = "http://localhost:3000/api/phone/users";
    // public static string BillsUrl = "http://localhost:3000/api/phone/bills";
    // public static string GetBillDetailsUrl(string yearMonth) => $"http://localhost:3000/api/phone/bills/{yearMonth}";
    // public static string GetDownloadGenerateLinkUrl(string yearMonth) => $"http://localhost:3000/api/phone/links/bills/{yearMonth}";

    public static TimeSpan UsersCacheExpiry = new TimeSpan(10, 0, 0);
    public static TimeSpan BillCacheExpiry = new TimeSpan(10, 0, 0);
    public static TimeSpan BillDetailsCacheExpiry = new TimeSpan(10, 0, 0);
    public static TimeSpan DownloadUrlCacheExpiry = new TimeSpan(0, 45, 0);

}