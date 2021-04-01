namespace web.Repository
{
    interface ISettingsProvider
    {
        string GetUserUrl();
        string GetBillsUrl();
        string GetBillDetailsUrl(string yearMonth);
        string GetDownloadUrl(string yearMonth);
    }
}