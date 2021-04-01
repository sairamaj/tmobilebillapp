namespace SelfService.Server.Models
{
    class ConnectionInfo
    {
        public string ClientId {get; set;}
        public string ClientSecret {get; set;}
        public string TenantId {get; set;}
        public string StorageConnectionString { get; set; }
    }
}