#
# Global constraints for WVCP
#


def arg_max(model, y, x):
  """
  Ensure that y = min({i in range(len(x)) | x[i]=max(x)})
  """
  assert len(x) != 0, f"`x` must not be empty"
  l = 0
  u = len(x) - 1
  n = u - l + 1
  xs = [model.NewIntVar((u-i)+n*x[i].Proto().domain[0], (u-i)+n*x[i].Proto().domain[1], 'xs%i' % i) for i in range(l,u+1)]
  for i in range(l,u+1):
    model.Add(xs[i] == n * x[i] + (u - i))

  lbMx = min([xs[i].Proto().domain[0] for i in range(l,u+1)])
  ubMx = max([xs[i].Proto().domain[1] for i in range(l,u+1)])
  Mx = model.NewIntVar(lbMx, ubMx, 'Mx')
  model.AddMaxEquality(Mx, xs)

  for i in range(l,u+1):
    b = model.NewBoolVar('')
    model.Add(y != i).OnlyEnforceIf(b)
    model.Add(y == i).OnlyEnforceIf(b.Not())
    model.Add(Mx > xs[i]).OnlyEnforceIf(b)
    model.Add(Mx <= xs[i]).OnlyEnforceIf(b.Not())


def arg_min(model, y, x):
  """
  Ensure that y = min({i in range(len(x)) | x[i]=min(x)})
  """
  assert len(x) != 0, f"`x` must not be empty"
  l = 0
  u = len(x) - 1
  n = u - l + 1
  xs = [model.NewIntVar(i+n*x[i].Proto().domain[0], i+n*x[i].Proto().domain[1], 'xs%i' % i) for i in range(l,u+1)]
  for i in range(l,u+1):
    model.Add(xs[i] == n * x[i] + i)

  lbMx = min([xs[i].Proto().domain[0] for i in range(l,u+1)])
  ubMx = max([xs[i].Proto().domain[1] for i in range(l,u+1)])
  Mx = model.NewIntVar(lbMx, ubMx, 'Mx')
  model.AddMinEquality(Mx, xs)

  for i in range(l,u+1):
    b = model.NewBoolVar('')
    model.Add(y != i).OnlyEnforceIf(b)
    model.Add(y == i).OnlyEnforceIf(b.Not())
    model.Add(Mx < xs[i]).OnlyEnforceIf(b)
    model.Add(Mx >= xs[i]).OnlyEnforceIf(b.Not())


def arg_max_no_zeros(model, j, y, x):
  """
  Ensure that
  - y = arg_max(x) if max(x)!=0
  - y = j + len(x) if max(x)=0
  """
  assert len(x) != 0, f"`x` must not be empty"
  assert j>=0, f"`j`>=0"
  z = model.NewIntVar(0, len(x)-1, 'z')
  arg_max(model, z, x)
  b = model.NewBoolVar('')
  xz = model.NewBoolVar('xz')
  model.AddElement(z, x, xz)
  model.Add(xz == 0).OnlyEnforceIf(b)
  model.Add(xz != 0).OnlyEnforceIf(b.Not())
  model.Add(y == j+len(x)).OnlyEnforceIf(b)
  model.Add(y == z).OnlyEnforceIf(b.Not())
