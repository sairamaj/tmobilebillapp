using System;

namespace SelfService.Server
{
    internal class Constants
    {
        public static TimeSpan UsersCacheExpiry = new TimeSpan(10, 0, 0);
        public static TimeSpan BillCacheExpiry = new TimeSpan(10, 0, 0);
        public static TimeSpan BillDetailsCacheExpiry = new TimeSpan(10, 0, 0);
        public static TimeSpan DownloadUrlCacheExpiry = new TimeSpan(0, 5, 0);
        public static TimeSpan UserRolesCacheExpiry = new TimeSpan(0, 15, 0);
    }
}