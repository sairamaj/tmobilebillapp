using System;
using System.Threading.Tasks;

namespace web.Shared
{
    internal interface ICacheManager
    {
        Task<T> GetWithSet<T>(string key, TimeSpan expiry, Func<Task<T>> func);
    }
}