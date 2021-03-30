internal static class UrlConstants{
    public static string UsersUrl = "http://localhost:3000/api/phone/users";
    public static string BillsUrl = "http://localhost:3000/api/phone/bills";
    public static string GetBillDetailsUrl(string yearMonth) => $"http://localhost:3000/api/phone/bills/{yearMonth}";
    public static string GetDownloadGenerateLinkUrl(string yearMonth) => $"http://localhost:3000/api/phone/links/bills/{yearMonth}";

}